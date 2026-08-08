import boto3
import json


def test_secrets_manager_access():
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.list_secrets(MaxResults=1)
    return response

# AWS Configuration
AWS_REGION = "us-east-1"
DYNAMODB_TABLE_NAME = "resume_data"
S3_BUCKET_NAME = "skimos-flask-app"  # ✅ Ensure this is set correctly.

# ✅ Use default credential chain (EC2 IAM Role)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

cloudwatch = boto3.client("cloudwatch", region_name=AWS_REGION)
s3_client = boto3.client("s3", region_name=AWS_REGION)

# ✅ S3 Upload Helper
def upload_file_to_s3(file, filename, bucket_name=S3_BUCKET_NAME):
    """Uploads a file to S3 and returns the file URL"""
    try:
        s3_client.upload_fileobj(file, bucket_name, filename)
        file_url = f"https://{bucket_name}.s3.{AWS_REGION}.amazonaws.com/{filename}"
        return {"message": "File uploaded successfully", "file_url": file_url}
    except Exception as e:
        return {"error": str(e)}

# ✅ S3 List Helper
def list_files_in_s3(bucket_name=S3_BUCKET_NAME):
    """Lists all files in the S3 bucket"""
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        if "Contents" not in response:
            return []  # Return empty list if no files found

        files = [
            {
                "name": obj["Key"],
                "size": obj["Size"],
                "url": f"https://{bucket_name}.s3.{AWS_REGION}.amazonaws.com/{obj['Key']}"
            }
            for obj in response["Contents"]
        ]
        return files
    except Exception as e:
        return {"error": str(e)}

# ✅ S3 Delete Helper
def delete_file_from_s3(filename, bucket_name=S3_BUCKET_NAME):
    """Deletes a file from S3"""
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=filename)
        return {"message": f"File '{filename}' deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

