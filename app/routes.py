from datetime import date, datetime, time,timedelta
from typing import Optional
import time as time2

from fastapi import APIRouter, Body, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.gcs import upload_to_gcs
from app.models import Account, Calorie, Food, User
from app.prediction import predict_food_id
from app.schemas import (
    AccountCreate,
    FoodDetail,
    FoodList,
    FoodSummary,
    UserCreate,
    UserUpdate,
)
from app.security import get_current_account, get_hashed_password

router = APIRouter()


@router.post("/register")
def register(account: AccountCreate, db: Session = Depends(get_db)):
    # Check if the username or email is already registered
    existing_account = (
        db.query(Account)
        .filter(
            (Account.username == account.username) | (Account.email == account.email)
        )
        .first()
    )
    if existing_account:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )

    # Hash the password
    hashed_password = get_hashed_password(account.password)
    account.password = hashed_password

    # Add the new account to the database
    new_account = Account(**account.dict())
    db.add(new_account)
    db.commit()

    return {"message": "Registration successful"}


@router.post("/users")
def create_user(
    user: UserCreate = Body(...),
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
):
    existing_user = db.query(User).filter(User.id == current_account.id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    # Create a new user
    new_user = User(
        account_id=current_account.id,
        nama=current_account.nama,
        email=current_account.email,
        **user.dict(),
    )

    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}


@router.put("/users/{user_id}")
def update_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
):
    # Check if the user exists
    user = db.query(User).filter(User.account_id == current_account.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user is associated with the current account
    if user.account_id != current_account.id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this user")

    # Update the user's information
    for field, value in user_update.dict(exclude_unset=True).items():
        if field not in ["username", "password"]:
            setattr(user, field, value)

    user_update_dict = user_update.dict()

    # Update Account if name, username, email, or password is changed
    if "name" in user_update_dict and user_update_dict["name"]:
        current_account.nama = user_update.name
    if "username" in user_update_dict and user_update_dict["username"]:
        current_account.username = user_update.username
    if "email" in user_update_dict and user_update_dict["email"]:
        current_account.email = user_update.email
    if "password" in user_update_dict and user_update_dict["password"]:
        hashed_password = get_hashed_password(user_update.password)
        current_account.password = hashed_password

    user.updated_at = func.current_timestamp()
    current_account.updated_at = func.current_timestamp()
    db.commit()

    return {"message": "User updated successfully"}


@router.post("/users/profile-image")
def upload_profile_image(
    profile_image: UploadFile = File(...),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    # Upload profile image to GCS and get the public URL
    if profile_image:
        filename = f"profile_image/{current_account.id}"
        filename = filename + "." + profile_image.filename.split(".")[-1]
        image_url = upload_to_gcs(profile_image, filename)
    else:
        raise HTTPException(status_code=400, detail="No profile image provided")

    # Retrieve the current user from the database
    current_user = db.query(User).filter(User.account_id == current_account.id).first()

    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the profile_image_url field of the current user in the database
    current_user.profile_image_url = image_url
    current_user.updated_at = func.current_timestamp()
    db.commit()

    return {"message": "Profile image uploaded successfully", "image_url": image_url}


@router.put("/users/profile-image/{user_id}")
def update_profile_image(
    profile_image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
):
    # Upload profile image to GCS and get the public URL
    if profile_image:
        filename = f"profile_image/{current_account.id}"
        filename = filename + "." + profile_image.filename.split(".")[-1]
        image_url = upload_to_gcs(profile_image, filename)
    else:
        raise HTTPException(status_code=400, detail="No profile image provided")

    # Retrieve the current user from the database
    current_user = db.query(User).filter(User.account_id == current_account.id).first()

    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the profile_image_url field of the current user in the database
    current_user.profile_image_url = image_url
    current_user.updated_at = func.current_timestamp()

    db.commit()

    return {"message": "Profile image updated successfully", "image_url": image_url}


@router.get("/foods", response_model=FoodList)
def get_foods(
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
    type: Optional[str] = None,
):
    query = db.query(Food)
    if type:
        query = query.filter(Food.type == type)
    foods = query.all()
    food_list = FoodList(foods=[food.__dict__ for food in foods])
    return food_list

@router.get("/foods/daily")
def get_food_by_day(
    date: date,
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
) -> FoodSummary:
    user = db.query(User).filter(User.account_id == current_account.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id

    calories = (
        db.query(Calorie)
        .filter(func.DATE(Calorie.created_at) == date, Calorie.user_id == user_id)
        .all()
    )

    food_details = []
    total_by_type = {}

    for calorie in calories:
        food = db.query(Food).filter(Food.id == calorie.food_id).first()
        if food:
            food_detail = FoodDetail(
                food_id=food.id, name=food.name, jumlah_kalori=food.jumlah_kalori
            )
            food_details.append(food_detail)

            if food.type not in total_by_type:
                total_by_type[food.type] = food.jumlah_kalori
            else:
                total_by_type[food.type] += food.jumlah_kalori

    food_summary = FoodSummary(food_details=food_details, total_by_type=total_by_type)

    return food_summary


@router.post("/calories")
def record_calorie_consumption(
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
    image: UploadFile = File(...),
):
    # Upload the image file to Google Cloud Storage (GCS) and get the public URL
    if image:
        filename = f"food_inference/{current_account.username}/{int(time2.time())}"
        filename = filename + "." + image.filename.split(".")[-1]
        image_url = upload_to_gcs(image, filename)
    else:
        raise HTTPException(status_code=400, detail="No image provided")

    food_id = predict_food_id(image_url)

    # Check if the food type exists
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    # Retrieve the user based on the current account ID
    user = db.query(User).filter(User.account_id == current_account.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a new calorie record
    new_calorie = Calorie(
        user_id=user.id,
        food_id=food_id,
        jumlah_kalori=food.jumlah_kalori,
        food_image_url=image_url,
    )

    db.add(new_calorie)
    db.commit()
    db.refresh(new_calorie)

    return {
        "message": "Calorie consumption recorded successfully",
        "calorie_id": new_calorie.id,
    }


@router.get("/calories/summary-day")
def get_daily_calorie_summary(
    date: date = Query(date.today(), description="Date for the summary"),
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
):
    # Calculate the start and end of the day
    start_date = datetime.combine(date, time.min)
    end_date = datetime.combine(date, time.max)

    # Retrieve the user based on the current account ID
    user = db.query(User).filter(User.account_id == current_account.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Calculate age based on birthdate
    birthdate = user.birthdate
    age = (date - birthdate) // timedelta(days=365.2425)  # Approximation for leap years

    # Compute target_kalori based on gender and user's information
    gender = user.gender.lower()
    weight = float(user.berat_badan)
    height = float(user.tinggi_badan)

    if gender == "male":
        target_kalori = 66.5 + (13.75 * weight) + (5.003 * height) - (6.75 * age)
    elif gender == "female":
        target_kalori = 655.1 + (9.563 * weight) + (1.85 * height) - (4.676 * age)
    else:
        target_kalori = 0

    # Query the database to get the calorie consumption summary for the day
    summary = (
        db.query(func.sum(Calorie.jumlah_kalori).label("total_kalori_masuk"))
        .filter(
            Calorie.user_id == user.id,
            Calorie.created_at >= start_date,
            Calorie.created_at <= end_date,
        )
        .first()
    )

    total_kalori_masuk = float(summary[0]) if summary[0] else 0
    total_kalori_kurang = (
        target_kalori - total_kalori_masuk if total_kalori_masuk < target_kalori else 0
    )
    total_kalori_berlebih = (
        total_kalori_masuk - target_kalori if total_kalori_masuk > target_kalori else 0
    )

    return {
        "total_kalori_masuk": total_kalori_masuk,
        "total_kalori_kurang": total_kalori_kurang,
        "total_kalori_berlebih": total_kalori_berlebih,
        "target_kalori": target_kalori,
    }


@router.get("/calories/summary-week")
def get_weekly_calorie_summary(
    start_date: date = Query(None, description="Start date for the summary"),
    end_date: date = Query(None, description="End date for the summary"),
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
):
    if not start_date or not end_date:
        # Calculate the start and end dates for the week
        start_date = date.today() - timedelta(days=date.today().weekday())
        end_date = start_date + timedelta(days=6)

    # Retrieve the user based on the current account ID
    user = db.query(User).filter(User.account_id == current_account.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Query the database to get the calorie consumption summary for the week
    summary = (
        db.query(
            func.DATE(Calorie.created_at).label("daily"),
            func.sum(Calorie.jumlah_kalori).label("total_kalori_masuk"),
        )
        .filter(
            Calorie.user_id == user.id,
            Calorie.created_at >= start_date,
            Calorie.created_at < end_date + timedelta(1),
        )
        .group_by(func.DATE(Calorie.created_at))
        .order_by(func.DATE(Calorie.created_at))
        .all()
    )

    date_list = []
    current_date = start_date

    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)

    summary_dict = {}
    for dt, total_kalori_masuk in summary:
        summary_dict[dt.strftime("%Y%m%d")] = float(total_kalori_masuk)

    summary_list = []
    for dt in date_list:
        summary_list.append(
            {
                "date": dt,
                "total_kalori_masuk": summary_dict.get(dt.strftime("%Y%m%d"), 0),
            }
        )

    return summary_list


# Dummy API - To be implemented
# This endpoint will eventually perform ML inference to determine the food_id
# For now, it randomly selects a food_id from the Food table
# Process the food image and perform machine learning inference
@router.post("/inference/food-id")
def infer_food_id(image_url: str, db: Session = Depends(get_db)):
    food = db.query(Food).order_by(func.random()).first()

    if not food:
        raise HTTPException(status_code=404, detail="No food found")

    return {"food_id": food.id}
