import logging
import boto3
from botocore.config import Config

class S3Client():

    """ This 
    """
    def __init__(self, region_name, bucket_name):
        # default will use the env access key and secret
        self.config =  Config(
            region_name = region_name,
        )
        self.bucket_name = bucket_name
    
    def upload_file(self, file_path, s3_path):
        s3_client = boto3.client('s3', config=self.config)
        try:
            s3_client.upload_file(file_path, self.bucket_name, s3_path)
            logging.info(f"Uploaded {file_path} to s3://{self.bucket_name}/{s3_path}")
        except Exception as e:
            logging.error(f"Error in uploading {file_path} to S3: {e}")