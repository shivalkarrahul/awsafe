import os
import json
from botocore.exceptions import ClientError

def check_public_access(bucket, s3_resource):
    bucket_name = bucket["Name"]

    try:
        bpa = s3_resource.client.get_public_access_block(Bucket=bucket_name)
        config = bpa.get("PublicAccessBlockConfiguration", {})
        
        # Check if all Block Public Access flags are True
        if all([
            config.get("BlockPublicAcls", False),
            config.get("IgnorePublicAcls", False),
            config.get("BlockPublicPolicy", False),
            config.get("RestrictPublicBuckets", False)
        ]):
            return {
                "rule_id": "S3_PUBLIC_ACCESS",
                "status": "PASS",
                "message": "Bucket does not allow public access"
            }
        else:
            return {
                "rule_id": "S3_PUBLIC_ACCESS",
                "status": "FAIL",
                "message": "Bucket allows some form of public access (BlockPublicAccess not fully enabled)"
            }

    except ClientError as e:
        # If no Public Access Block is configured, treat as FAIL
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            return {
                "rule_id": "S3_PUBLIC_ACCESS",
                "status": "FAIL",
                "message": "Bucket has no Public Access Block configuration"
            }
        else:
            raise e


def check_encryption(bucket, s3_resource):
    enc = s3_resource.get_bucket_encryption(bucket["Name"])
    if enc:
        return {
            "rule_id": "S3_ENCRYPTION",
            "status": "PASS",
            "message": "Bucket has encryption enabled"
        }
    else:
        return {
            "rule_id": "S3_ENCRYPTION",
            "status": "FAIL",
            "message": "Bucket has no encryption enabled"
        }
    

RULES = {
    "S3_PUBLIC_ACCESS": check_public_access,
    "S3_ENCRYPTION": check_encryption
}

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/rules_config.json")
with open(CONFIG_PATH, "r") as f:
    RULES_CONFIG = json.load(f)

def run_all_rules(bucket, s3_resource):
    results = []
    for rule_id, rule_function in RULES.items():
        if RULES_CONFIG.get(rule_id, True):
            results.append(rule_function(bucket, s3_resource))
    return results