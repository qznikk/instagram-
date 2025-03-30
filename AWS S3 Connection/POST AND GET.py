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

# Initialize Amazon S3 client
s3_client = boto3.client(
    service_name="s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

DEFAULT_FOLDER = "my_folder"  # Default folder


@app.route("/upload", methods=["POST"])
def upload_to_s3():
    data = request.get_json()
    if not data or "file_name" not in data:
        return jsonify({"error": "Invalid request. 'file_name' is required"}), 400

    file_path = data["file_name"]
    folder_name = data.get("folder", DEFAULT_FOLDER)

    # Sanitize folder name
    folder_name = secure_filename(folder_name)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 400

    filename = secure_filename(os.path.basename(file_path))

    try:
        with open(file_path, "rb") as file:
            file_key = f"{folder_name}/{filename}"
            s3_client.upload_fileobj(file, AWS_BUCKET_NAME, file_key)

        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
        return jsonify({"message": "File uploaded", "url": file_url, "folder": folder_name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def list_files_in_bucket():
    """Lists all files in the S3 bucket."""
    response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
    return [obj["Key"] for obj in response.get("Contents", [])]


def download_file_from_s3(file_key, download_folder):
    """Downloads a file from S3 to the specified folder."""
    try:
        filename = os.path.basename(file_key)
        os.makedirs(download_folder, exist_ok=True)
        download_path = os.path.join(download_folder, filename)

        s3_client.download_file(AWS_BUCKET_NAME, file_key, download_path)
        return f"Downloaded: {file_key} → {download_path}"
    except Exception as e:
        return f"Error downloading {file_key}: {e}"


@app.route("/download", methods=["POST"])
def download_files():
    """Downloads all files from a specified S3 folder."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        folder_name = data.get("folder")
        if not folder_name:
            return jsonify({"error": "Folder name is required"}), 400

        # List all files in the bucket
        all_files = list_files_in_bucket()
        filtered_files = [file for file in all_files if file.startswith(folder_name + "/")]

        if not filtered_files:
            return jsonify({"message": f"No files found in folder '{folder_name}'"}), 404

        # Download selected files
        download_folder = f"C:/Users/machm/zdjecia/{folder_name}"
        results = [download_file_from_s3(file, download_folder) for file in filtered_files]

        return jsonify({"status": "Completed", "files": results})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
