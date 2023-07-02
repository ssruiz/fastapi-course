import boto3
from decouple import config


class S3Service:
    def __init__(self):
        self.key = config("AWS_ACCESS_KEY")
        self.secret = config("AWS_SECRET_KEY")
        self.s3 = boto3.client("s3", aws_access_key_id=self.key, aws_secret_access_key=self.secret)
        self.bucket = config("ASW_S3_BUCKET")
        self.region = config("AWS_S3_REGION")

    def upload(self, path, key, ext):
        self.s3.upload_file(
            path,
            self.bucket,
            key,
            ExtraArgs={"ACL": "public-read", "ContentType": f"image/{ext}"})
        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
