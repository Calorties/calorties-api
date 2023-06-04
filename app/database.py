import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/db-calorie-tracking"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
