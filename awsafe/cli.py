import click
from awsafe.resources.ec2 import EC2Resource
from awsafe.rules.ec2_rules import check_public_ip

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

    for i in instances:
        iid = i.get("InstanceId")
        itype = i.get("InstanceType")
        state = i.get("State", {}).get("Name")
        public_ip = i.get("PublicIpAddress", "-")
        click.echo(f"- {iid}  |  {itype}  |  {state}  |  public_ip: {public_ip}")

    for i in instances:
        iid = i.get("InstanceId")
        click.echo(f"Instance: {iid}")
        rule_result = check_public_ip(i)

        click.echo(f"  Rule: {rule_result['rule_id']}")
        click.echo(f"  Status: {rule_result['status']}")
        click.echo(f"  Message: {rule_result['message']}\n")     



@cli.group()
def report():
    pass

@report.command()
def ec2_report():
    click.echo("Report EC2")


if __name__ == "__main__":
    cli()