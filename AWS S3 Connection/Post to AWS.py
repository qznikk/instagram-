import boto3
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# AWS Config
AWS_ACCESS_KEY = "key"
AWS_SECRET_KEY = "key"
AWS_BUCKET_NAME = "igdatabase"
AWS_REGION = "eu-north-1"

# S3 client initialization
s3_client = boto3.client(
    service_name="s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

DEFAULT_FOLDER = "my_folder"  # Default folder name in the S3 bucket

@app.route("/upload", methods=["POST"])
def upload_to_s3():
    # Ensure JSON request
    data = request.get_json()
    if not data or "file_name" not in data:
        return jsonify({"error": "Invalid request. 'file_name' is required"}), 400

    file_path = data["file_name"]
    folder_name = data.get("folder", DEFAULT_FOLDER)

    # Ensure folder name is safe
    folder_name = secure_filename(folder_name)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 400

    filename = secure_filename(os.path.basename(file_path))

    try:
        # Open file and upload to S3
        with open(file_path, "rb") as file:
            file_key = f"{folder_name}/{filename}"
            s3_client.upload_fileobj(file, AWS_BUCKET_NAME, file_key)

        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
        return jsonify({"message": "File uploaded", "url": file_url, "folder": folder_name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)