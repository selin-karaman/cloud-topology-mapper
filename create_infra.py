import boto3
import zipfile
import io

endpoint = "http://localhost:4566"
region = "us-east-1"
auth = {"aws_access_key_id": "test", "aws_secret_access_key": "test", "region_name": region}

def create_lambda_zip():
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zipper:
        handler_code = "def handler(event, context):\n    return {'statusCode': 200}"
        zipper.writestr("index.py", handler_code)
    return zip_buffer.getvalue()

def setup():
    s3 = boto3.client("s3", endpoint_url=endpoint, **auth)
    
    bucket_name = "cloud-club-data"
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"✅ S3: '{bucket_name}' created.")
    except Exception as e:
        print(f"ℹ️ S3 Info: {e}")

    sqs = boto3.client("sqs", endpoint_url=endpoint, **auth)
    try:
        sqs.create_queue(QueueName="task-queue")
        print("✅ SQS: 'task-queue' is ready.")
    except Exception as e:
        print(f"ℹ️ SQS Info: {e}")

    lmb = boto3.client("lambda", endpoint_url=endpoint, **auth)
    try:
        lmb.create_function(
            FunctionName="process-image",
            Runtime="python3.9",
            Handler="index.handler",
            Role="arn:aws:iam::000000000000:role/irrelevant",
            Code={'ZipFile': create_lambda_zip()}
        )
        print("✅ Lambda: 'process-image' created.")
    except lmb.exceptions.ResourceConflictException:
        print("ℹ️ Lambda: 'process-image' already exists.")
    except Exception as e:
        print(f"❌ Lambda Error: {e}")

if __name__ == "__main__":
    setup()