import boto3

class EC2Resource:
    def __init__(self, region="us-east-1",):
        self.client = boto3.client("ec2", region_name=region)


    def get_instances(self):
        response = self.client.describe_instances()
        instances = []
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instances.append(instance)
        return instances



