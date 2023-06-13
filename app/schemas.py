from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    nama: str = Field(None, min_length=1, max_length=255)
    username: str = Field(None, min_length=1, max_length=255)
    email: str = Field(None, min_length=1, max_length=255)
    password: str = Field(None, min_length=1, max_length=255)


class UserCreate(BaseModel):
    birthdate: date = Field(..., description="Date of birth (YYYY-MM-DD)")
    gender: str = Field(None, enum=["Male", "Female"])
    tinggi_badan: float = Field(None, ge=0)
    berat_badan: float = Field(None, ge=0)


class UserUpdate(BaseModel):
    nama: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[str] = Field(None, min_length=1, max_length=255)
    username: Optional[str] = Field(None, min_length=1, max_length=255)
    password: Optional[str] = Field(None, min_length=1, max_length=255)
    birthdate: Optional[date] = Field(None, description="Date of birth (YYYY-MM-DD)")
    gender: Optional[str] = Field(None, enum=["Male", "Female"])
    tinggi_badan: Optional[float] = Field(None, ge=0)
    berat_badan: Optional[float] = Field(None, ge=0)
    profile_image_url: Optional[str] = Field(None, min_length=1, max_length=255)


class FoodItem(BaseModel):
    id: int
    name: str
    type: str
    jumlah_kalori: int
    thumbnail: Optional[str] = Field(None, min_length=1, max_length=255)


class FoodList(BaseModel):
    foods: List[FoodItem]


class FoodDetail(BaseModel):
    food_id: int
    name: str
    jumlah_kalori: int
    thumbnail: Optional[str] = Field(None, min_length=1, max_length=255)


class FoodSummary(BaseModel):
    food_details: List[FoodDetail]
    total_by_type: Dict[str, int]
