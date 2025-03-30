import boto3
from flask import Flask, request, jsonify
import os
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# AWS Config
AWS_ACCESS_KEY = "key"
AWS_SECRET_KEY = "key"
AWS_BUCKET_NAME = "igdatabase"
AWS_REGION = "eu-north-1"

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

WATERMARKED_FOLDER = "watermarked"  # Folder in S3 for processed images

def add_text_watermark(image_path, watermark_text="Watermark"):
    """Applies a text watermark to an image and returns the new file path."""
    image = Image.open(image_path).convert("RGBA")
    watermark_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark_layer)

    # Load default font (you can use a custom .ttf file)
    font = ImageFont.load_default()

    # Define text position
    position = (10, 10)
    draw.text(position, watermark_text, font=font, fill=(255, 255, 255, 128))

    # Merge watermark with the image
    watermarked_image = Image.alpha_composite(image, watermark_layer)

    # Save the new image
    watermarked_path = f"watermarked_{os.path.basename(image_path)}"
    watermarked_image.convert("RGB").save(watermarked_path, "JPEG")

    return watermarked_path

@app.route("/upload", methods=["POST"])
def upload_to_s3():
    data = request.get_json()
    if not data or "file_name" not in data:
        return jsonify({"error": "Invalid request. 'file_name' is required"}), 400

    file_path = data["file_name"]
    watermark_text = data.get("watermark", "Watermark")  # Default watermark if not provided

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 400

    try:
        # Apply watermark
        watermarked_file = add_text_watermark(file_path, watermark_text)

        # Upload to S3 in the 'watermarked' folder
        file_key = f"{WATERMARKED_FOLDER}/{os.path.basename(watermarked_file)}"
        with open(watermarked_file, "rb") as file:
            s3_client.upload_fileobj(file, AWS_BUCKET_NAME, file_key)

        # Generate S3 file URL
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"

        # Cleanup local watermarked file
        os.remove(watermarked_file)

        return jsonify({"message": "File uploaded and watermarked", "url": file_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
