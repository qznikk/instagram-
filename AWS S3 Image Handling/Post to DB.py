import boto3
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# AWS Config
AWS_ACCESS_KEY = "ath_key"
AWS_SECRET_KEY = "sercet_key"
AWS_BUCKET_NAME = "igdatabase"
AWS_REGION = "eu-north-1"  # Stockholm region

# S3 client initialization
s3_client = boto3.client(
    service_name='s3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Folder name in the bucket
FOLDER_NAME = "my_folder"  # Nazwa folderu jaki chcemy stworzyc

@app.route("/")
def home():
    return "Welcome to the Image Upload API!"


@app.route("/upload", methods=["POST"])
def upload_to_s3():
    # Check if the 'file' is in the request
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # Check if the file has a valid name
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    print(f"Uploading file: {filename}")  # Debugging log to see the filename

    try:
        # Upload file to S3 (e.g., my_folder/filename)
        file_key = f"{FOLDER_NAME}/{filename}"

        # Upload file to the specified folder in S3
        s3_client.upload_fileobj(file, AWS_BUCKET_NAME, file_key)

        # Construct the URL to access the uploaded file
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"

        return jsonify({"message": "File uploaded", "url": file_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def upload_file_directly(file_path):

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        try:
            # Get the filename and define the file key
            filename = os.path.basename(file_path)
            file_key = f"{FOLDER_NAME}/{filename}"

            # Upload file to S3
            s3_client.upload_fileobj(file, AWS_BUCKET_NAME, file_key)

            # Construct the URL to access the uploaded file
            file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"

            return file_url
        except Exception as e:
            return str(e)


@app.route("/upload_from_script", methods=["POST"])
def upload_from_script():
    """
    This route will trigger the file upload directly from the code without needing Postman.
    """
    # Path to the file you want to upload (adjust the path)
    file_path = 'C:/Users/machm/OneDrive/Obrazy/Zrzuty ekranu/Screenshot 2024-12-14 181919.png'  # Change this to your local image path

    # Upload the file directly
    file_url = upload_file_directly(file_path)

    # Return the result
    return jsonify({"message": "File uploaded from script", "url": file_url}), 200


if __name__ == "__main__":
    app.run(debug=True)
