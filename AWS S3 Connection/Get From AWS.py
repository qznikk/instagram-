from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# AWS Config
AWS_ACCESS_KEY = "key"
AWS_SECRET_KEY = "key"
AWS_BUCKET_NAME = "igdatabase"
AWS_REGION = "eu-north-1"

# Initialize Amazon S3 client
s3_client = boto3.client(
    service_name='s3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)


# List files in the S3 bucket
def list_files_in_bucket():
    response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
    return [obj["Key"] for obj in response.get("Contents", [])]


# Download a file from S3
def download_file_from_s3(file_key, download_folder):
    try:
        filename = os.path.basename(file_key)  # Extract the filename
        os.makedirs(download_folder, exist_ok=True)  # Ensure folder exists
        download_path = os.path.join(download_folder, filename)

        s3_client.download_file(AWS_BUCKET_NAME, file_key, download_path)
        return f"Downloaded: {file_key} → {download_path}"
    except Exception as e:
        return f"Error downloading {file_key}: {e}"


@app.route('/download', methods=['POST'])
def download_files():
    print("Request Headers:", request.headers)
    print("Request Body:", request.get_data())  # This prints the raw body
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        folder_name = data.get('folder')
        if not folder_name:
            return jsonify({"error": "Folder name is required"}), 400

        # List all files in the bucket
        all_files = list_files_in_bucket()

        # Filter files that start with the specified folder name
        filtered_files = [file for file in all_files if file.startswith(folder_name + "/")]

        if not filtered_files:
            return jsonify({"message": f"No files found in folder '{folder_name}'"}), 404

        # Download selected files
        download_folder = f"C:/Users/machm/zdjecia/{folder_name}"
        results = [download_file_from_s3(file, download_folder) for file in filtered_files]

        return jsonify({"status": "Completed", "files": results})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
