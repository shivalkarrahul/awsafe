import click
from awsafe.resources.ec2 import EC2Resource
from awsafe.rules.ec2_rules import run_all_rules

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

    for i in instances:
        iid = i.get("InstanceId")
        iname = get_instance_name(i)
        results = run_all_rules(i)
        click.echo(f"\nInstance: {iid} (Name: {iname})")
        for rule_results in results:
            status = rule_results["status"]
            if status == "PASS":
                colored_status = click.style(status, fg="green")
            elif status == "FAIL":
                colored_status = click.style(status, fg="red")
            else:
                colored_status = click.style(status, fg="yellow")

            click.echo(
                f"  Rule: {rule_results['rule_id']:<20} | "
                f"Status: {colored_status:<5} | "
                f"Message: {rule_results['message']}"
            )
        click.echo("")  #


@cli.group()
def report():
    pass

@report.command()
def ec2_report():
    click.echo("Report EC2")


if __name__ == "__main__":
    cli()