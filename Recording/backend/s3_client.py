import boto3

# The access credentials for S3
s3 = boto3.client(
    's3',
    aws_access_key_id='your-key',
    aws_secret_access_key='your-key',
    region_name='your-region'  # region
)