from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.models import Account
from app.security import create_access_token, get_current_account, verify_password

router = APIRouter()


@router.post("/login")
def login(username: str, password: str, db=Depends(get_db)):
    account = db.query(Account).filter(Account.username == username).first()
    if not account:
        raise HTTPException(status_code=404, detail="Username not found")
    if not verify_password(password, account.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Generate JWT token
    access_token = create_access_token(data={"sub": account.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(current_account: Account = Depends(get_current_account)):

    return {"message": "Logout successful"}
