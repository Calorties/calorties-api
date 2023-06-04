from fastapi import UploadFile
from google.cloud import storage


def upload_to_gcs(file: UploadFile, filename) -> str:
    # Create a GCS client
    key_path = "service-account.json"
    client = storage.Client.from_service_account_json(key_path)

    # Set up GCS bucket and filename
    bucket_name = "calorties"

    # Upload the file to GCS
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_file(file.file, content_type=file.content_type)

    # Get the public URL of the uploaded file
    image_url = blob.public_url

    return image_url
