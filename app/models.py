from sqlalchemy import (
    DECIMAL,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Account(Base):
    __tablename__ = "Account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(
        DateTime, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP"
    )
    deleted_at = Column(DateTime)


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("Account.id"))
    nama = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    birthdate = Column(Date)
    gender = Column(Enum("Male", "Female", "Other"))
    tinggi_badan = Column(DECIMAL(5, 2))
    berat_badan = Column(DECIMAL(5, 2))
    profile_image_url = Column(String(255))
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(
        DateTime, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP"
    )
    deleted_at = Column(DateTime)
    account = relationship("Account", foreign_keys=[account_id])


class Food(Base):
    __tablename__ = "Food"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(String(255))
    jumlah_kalori = Column(Integer)
    thumbnail = Column(String(255))
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(
        DateTime, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP"
    )
    deleted_at = Column(DateTime)


class Calorie(Base):
    __tablename__ = "Calorie"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    food_id = Column(Integer, ForeignKey("Food.id"))
    jumlah_kalori = Column(Integer)
    food_image_url = Column(String(255))
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(
        DateTime, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP"
    )
    deleted_at = Column(DateTime)
    user = relationship("User", foreign_keys=[user_id])
    food = relationship("Food", foreign_keys=[food_id])
