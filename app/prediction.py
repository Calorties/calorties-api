import os

from app.config import INFERENCE

import requests
from fastapi import HTTPException, UploadFile


def predict_food(image_file: UploadFile):
    infer_food_endpoint = INFERENCE

    headers = {
        "accept": "application/json",
    }

    image_file.file.seek(0)

    files = {
        "file": (image_file.filename, image_file.file, image_file.content_type),
    }

    response = requests.post(infer_food_endpoint, headers=headers, files=files)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    result = response.json()
    food = result.get("predicted_food")

    return food
