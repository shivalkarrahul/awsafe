import json
import os

def check_public_ip(instance):

    if "PublicIpAddress" in instance:
        return {
            "rule_id": "EC2_PUBLIC_IP",
            "status": "FAIL",
            "message": "Instance has a public IP address"
        }

    return {
    "rule_id": "EC2_PUBLIC_IP",
    "status": "PASS",
    "message": "No public IP found"
}        

def check_instance_type(instance):
    allowed_instance_types = ["t2.micro", "t3.micro"]

    if instance.get("InstanceType") not in allowed_instance_types:
        return {
            "rule_id": "EC2_INSTANCE_TYPE",
            "status": "FAIL",
            "message": f"Instance type {instance.get('InstanceType')} is not allowed"
        }        
    
    return {
        "rule_id": "EC2_INSTANCE_TYPE",
        "status": "PASS",
        "message": f"Instance type {instance.get('InstanceType')} is allowed"
    }

def check_iam_role(instance):
    if instance.get("IamInstanceProfile"):
        return {
            "rule_id": "EC2_IAM_ROLE", 
            "status": "PASS", 
            "message": "IAM role attached"}
    
    return {
        "rule_id": "EC2_IAM_ROLE", 
        "status": "FAIL", 
        "message": "No IAM role attached"}



RULES = {
    "EC2_PUBLIC_IP": check_public_ip,
    "EC2_INSTANCE_TYPE": check_instance_type,
    "EC2_IAM_ROLE": check_iam_role
}

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/rules_config.json")
with open(CONFIG_PATH, "r") as f:
    RULES_CONFIG = json.load(f)

def run_all_rules(instance):
    results = []
    for rule_id, rule_function in RULES.items():
        if RULES_CONFIG.get(rule_id, True):
            results.append(rule_function(instance))
    return results
