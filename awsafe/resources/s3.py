import boto3

class S3Resource:
    def __init__(self):
        self.client = boto3.client("s3")

    def list_buckets(self):
        response = self.client.list_buckets()
        return response.get("Buckets", [])
    
    def get_bucket_acl(self, bucket_name):
        response = self.client.get_bucket_acl(Bucket=bucket_name)
        return response    

    def get_bucket_encryption(self, bucket_name):
        try:
            response = self.client.get_bucket_encryption(Bucket=bucket_name)
            return response
        except self.client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                return None
            else:
                raise e    