import boto3

# AWS Config
AWS_ACCESS_KEY = "ath_key"
AWS_SECRET_KEY = "sercet_key" #AWS Secret Key, kazdy moze miec wlasny jak narazie
AWS_BUCKET_NAME = "igdatabase"  #S3 bucket name, igdatabase jak narazie
AWS_REGION = "eu-north-1"  #Region (Stockholm)

# Initialize session, Amazon S3
s3_client = boto3.client(
    service_name='s3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)


# List files in the bucket
def list_files_in_bucket():
    response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)

    if "Contents" in response:
        print("Files in the bucket:")
        for obj in response["Contents"]:
            print(obj["Key"])  # Print the file names (keys)
    else:
        print("No files found in the bucket.")


def download_file_from_s3(file_key, download_path):
    try:
        # Download the file from the bucket
        s3_client.download_file(AWS_BUCKET_NAME, file_key, download_path)
        print(f"File {file_key} downloaded successfully to {download_path}.")
    except Exception as e:
        print(f"Error downloading file: {e}")


if __name__ == "__main__":
    # List the files stored in S3 bucket
    list_files_in_bucket()

    # Specify the file you want to download
    file_key = 'my_folder/Screenshot 2024-12-14 181919.png'  # Example file path with spaces
    download_path = 'C:/sem6/SP/TEST/Screenshot_2024.png'  # Local path including file name


    # Download the file
    download_file_from_s3(file_key, download_path)
