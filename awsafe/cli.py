import click
from awsafe.resources.ec2 import EC2Resource

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
    
    click.echo(f"Found {len(instances)} instances.\n")

    for i in instances:
        iid = i.get("InstanceId")
        itype = i.get("InstanceType")
        state = i.get("State", {}).get("Name")
        public_ip = i.get("PublicIpAddress", "-")
        click.echo(f"- {iid}  |  {itype}  |  {state}  |  public_ip: {public_ip}")    
    




@cli.group()
def report():
    pass

@report.command()
def ec2_report():
    click.echo("Report EC2")


if __name__ == "__main__":
    cli()