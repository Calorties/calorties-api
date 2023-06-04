import requests
from fastapi import HTTPException


def predict_food_id(image_url):
    # Call infer_food_id endpoint to get the food_id based on the image URL
    infer_food_id_endpoint = "http://localhost:8000/inference/food-id"
    data = {"image_url": image_url}
    response = requests.post(infer_food_id_endpoint, params=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    result = response.json()
    food_id = result.get("food_id")

    return food_id
