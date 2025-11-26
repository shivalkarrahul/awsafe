import click
from awsafe.resources.ec2 import EC2Resource
from awsafe.rules.ec2_rules import run_all_rules as ec2_run_all_rules
from awsafe.resources.s3 import S3Resource
from awsafe.rules.s3_rules import run_all_rules as s3_run_all_rules

def get_instance_name(instance):
    tags = instance.get("Tags", [])
    for tag in tags:
        if tag["Key"] == "Name":
            name = tag["Value"].strip()
            if name:
                return name
    return "N/A"

@click.group()
def cli():
    pass


@cli.group()
def scan():
    pass

@scan.command()
@click.option("--region", default="us-east-1", show_default=True, help="AWS region to scan")
def ec2_scan(region):
    click.echo(f"Connecting to EC2 in region = {region}")
    scanner = EC2Resource(region)

    try:
        instances = scanner.get_instances()

    except Exception as e:
        click.echo(f"Error calling AWS EC2: {e}", err=True)
        raise SystemExit(1)
    
    click.echo(f"Found {len(instances)} instance/s.\n")

    total_rules = 0
    passed_rules = 0
    failed_rules = 0

    for i in instances:
        iid = i.get("InstanceId")
        iname = get_instance_name(i)
        results = ec2_run_all_rules(i)
        click.echo(f"\nInstance: {iid} (Name: {iname})")
        for rule_results in results:
            status = rule_results["status"]
            total_rules += 1
            if status == "PASS":
                colored_status = click.style(status, fg="green")
                passed_rules += 1
            elif status == "FAIL":
                colored_status = click.style(status, fg="red")
                failed_rules += 1
            click.echo(
                f"  Rule: {rule_results['rule_id']:<20} | "
                f"Status: {colored_status:<5} | "
                f"Message: {rule_results['message']}"
            )
        click.echo("")  #
    click.echo("\n================ SUMMARY ================")
    click.echo(f"Total Instances: {len(instances)}")
    click.echo(f"Total Rules Run: {total_rules}")
    click.echo(f"Passed: {passed_rules}")
    click.echo(f"Failed: {failed_rules}")
    click.echo("==========================================")
    click.echo("")  #

@scan.command()
@click.option("--region", default="us-east-1", show_default=True, help="AWS region to scan")
def s3_scan(region):
    click.echo("Scanning S3 buckets...\n")

    scanner = S3Resource()
    buckets = scanner.list_buckets()
    click.echo(f"Found {len(buckets)} bucket/s.\n")

    passed_rules = 0
    failed_rules = 0
    total_rules = 0

    for bucket in buckets:
        results = s3_run_all_rules(bucket, scanner)
        click.echo(f"\nBucket: {bucket['Name']}")
        for rule_results in results:
            status = rule_results['status']
            total_rules += 1
            if status == "PASS":
                colored_status = click.style(status, fg="green")
                passed_rules += 1
            elif status == "FAIL":
                colored_status = click.style(status, fg="red")
                failed_rules += 1
            click.echo(
                f"  Rule: {rule_results['rule_id']:<20} | "
                f"Status: {colored_status:<5} | "
                f"Message: {rule_results['message']}"
            )                
    click.echo("\n================ SUMMARY ================")
    click.echo(f"Total Buckets: {len(buckets)}")
    click.echo(f"Total Rules Run: {total_rules}")
    click.echo(f"Passed: {passed_rules}")
    click.echo(f"Failed: {failed_rules}")
    click.echo("==========================================\n")

if __name__ == "__main__":
    cli()