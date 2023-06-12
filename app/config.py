import os

from dotenv import load_dotenv

# Load Env Variables
load_dotenv()

# Cloud Sql
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
NAME = os.getenv("DB_NAME")

# Inference
INFERENCE = os.getenv("INFERENCE")

# Cloud Storage
BUCKET = os.getenv("BUCKET")
