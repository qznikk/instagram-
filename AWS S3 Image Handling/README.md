Below are the instructions for setting up and using the system, along with instructions for accessing the shared AWS S3 bucket.

### 1. Prerequisites

Before running the system, ensure you have the following installed:

: The programming language used to run the Flask API.

Flask: A lightweight web framework used to create the API.

Boto3: The AWS SDK for Python to interact with Amazon S3.

Postman (optional but recommended): To test API endpoints locally.

AWS Account: You need an AWS account to access the S3 bucket.

### 2. Setting Up AWS S3

To upload and download files from AWS S3, you'll first need to configure your S3 bucket. Here are the steps to set up AWS S3:

Sign in to AWS Management Console: Go to AWS Console and log in.

Create an S3 Bucket:

Navigate to S3 in the AWS Management Console.

Click on “Create Bucket”.

Give your bucket a unique name (e.g., my-upload-bucket).

Choose the AWS region closest to your location.

Click “Create Bucket” to finish.

Get your AWS Credentials:

Go to AWS IAM Console.

Create a new IAM user with programmatic access and assign appropriate permissions to S3 (e.g., AmazonS3FullAccess).

After creation, save the Access Key ID and Secret Access Key. You’ll use these in the Flask API configuration.

### 3. Flask API Setup

To use the file upload and download API, you need to set up a Python environment and install dependencies.

Setting Up Python Environment
Create a Virtual Environment (Optional but recommended):

python
Copy
Edit
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_KEY = "YOUR_AWS_SECRET_KEY"
AWS_BUCKET_NAME = "YOUR_S3_BUCKET_NAME"
AWS_REGION = "YOUR_S3_BUCKET_REGION"

### 4. Running the Flask Application

Start the Flask Application: To run the application, use the following command:

- Running on http://127.0.0.1:5000/

### 5. Using the API

You can use Postman or any API testing tool to interact with the API endpoints.

Upload File
Method: POST

URL: http://127.0.0.1:5000/upload

Body: Choose the form-data option and select file as the key. Upload a file

Response:
If successful, you will receive a message with the file URL:

Response:
The file will be returned as a downloadable response, and you can save it.

### 6. Accessing the Shared S3 Bucket

To allow others to upload and download files to/from your S3 bucket, follow these steps:

1. Granting Access via IAM User
   You can create IAM users for your friends and grant them access to the S3 bucket:

Go to IAM Console: IAM Console

Create a New IAM User for each of your friends:

Click "Users" on the left menu.

Click "Add user".

Provide a username and select "Programmatic access".

Assign Permissions:

Under “Set permissions,” choose “Attach existing policies directly”.

Select AmazonS3FullAccess or create a custom policy with specific permissions (e.g., s3:ListBucket, s3:PutObject, s3:GetObject).
