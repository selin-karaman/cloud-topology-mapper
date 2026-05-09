import time
import boto3
from rich.console import Console
from rich.tree import Tree
from src.discovery import DiscoveryEngine
from src.formatter import MapFormatter

console = Console()
engine = DiscoveryEngine()
formatter = MapFormatter()

def get_s3_to_sqs_relations():
    relations = []
    try:
        s3 = boto3.client("s3", endpoint_url="http://localhost:4566", region_name="us-east-1")
        buckets = s3.list_buckets().get('Buckets', [])
        
        for bucket in buckets:
            name = bucket['Name']
            notifications = s3.get_bucket_notification_configuration(Bucket=name)
            
            for queue_conf in notifications.get('QueueConfigurations', []):
                queue_arn = queue_conf['QueueArn']
                queue_name = queue_arn.split(':')[-1]
                relations.append({
                    "from": name,
                    "to": queue_name,
                    "type": "SNS/SQS Trigger"
                })
    except Exception:
        pass
    return relations

def run_app():
    try:
        while True:
            console.clear()
            console.print(formatter.create_header())

            topology_data = engine.get_topology()
            relations = get_s3_to_sqs_relations()

            infra_tree = formatter.generate_tree(topology_data)

            if relations:
                for rel in relations:
                    console.print(f"[bold cyan]🔗 Relation Detected:[/bold cyan] [yellow]{rel['from']}[/yellow] [bold green]──▶[/bold green] [magenta]{rel['to']}[/magenta]\n")

            console.print(infra_tree)
            console.print("\n[bold dim]🔄 Auto-refreshing every 5s... (Ctrl+C to stop)[/bold dim]")
            time.sleep(5)
            
    except KeyboardInterrupt:
        console.print("\n[bold red]Stopping Infra-Map... See you later![/bold red]")

if __name__ == "__main__":
    run_app()