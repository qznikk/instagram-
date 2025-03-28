from flask import Flask, request, jsonify
import boto3
from werkzeug.utils import secure_filename
import mimetypes

app = Flask(__name__)

# Set the maximum content length for uploads (e.g., 50MB)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

AWS_ACCESS_KEY = "ath_key"
AWS_SECRET_KEY = "sercet_key"
AWS_BUCKET_NAME = "igdatabase"
AWS_REGION = "eu-north-1"  # Stockholm region

s3_client = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mp3', 'wav', 'pdf', 'docx', 'pptx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_to_s3():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_key = f"uploads/{filename}"

        try:
            s3_client.upload_fileobj(file, AWS_BUCKET_NAME, file_key)
            file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
            return jsonify({"message": "File uploaded", "file_url": file_url}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "File type not allowed"}), 400


@app.route('/download/<file_key>', methods=['GET'])
def download_file(file_key):
    try:
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
        return jsonify({"file_url": file_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
