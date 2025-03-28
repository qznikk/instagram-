import boto3
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# AWS Config
AWS_ACCESS_KEY = "ath_key"
AWS_SECRET_KEY = "sercet_key" #AWS Secret Key, kazdy moze miec wlasny jak narazie
AWS_BUCKET_NAME = "igdatabase"  #S3 bucket name, igdatabase jak narazie
AWS_REGION = "eu-north-1"  #Region (Stockholm)

# S3 client initialization
s3_client = boto3.client(
    service_name='s3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

DEFAULT_FOLDER = "my_folder"  # Default folder name in the S3 bucket

@app.route("/")
def home():
    return "Welcome to the Image Upload API!"


@app.route("/upload", methods=["POST"])
def upload_to_s3():
    # Check if the file is in the request
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # Check if the file has a valid name
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)

    # Get folder name from the request (if provided), otherwise use the default folder
    folder_name = request.form.get("folder", DEFAULT_FOLDER)

    # Ensure folder name is safe
    folder_name = secure_filename(folder_name)

    print(f"Uploading file: {filename} to folder: {folder_name}")  # Debugging log

    try:
        # Upload file to the specified folder in S3
        file_key = f"{folder_name}/{filename}"
        s3_client.upload_fileobj(file, AWS_BUCKET_NAME, file_key)

        # Construct the URL to access the uploaded file
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"

        return jsonify({"message": "File uploaded", "url": file_url, "folder": folder_name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
