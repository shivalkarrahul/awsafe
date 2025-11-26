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
