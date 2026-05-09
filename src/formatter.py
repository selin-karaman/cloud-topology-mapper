from rich.tree import Tree
from rich.panel import Panel
from rich.console import Group
from rich.text import Text

class MapFormatter:
    @staticmethod
    def create_header():
        return Panel.fit(
            "[bold cyan]☁️ CLOUD-TOPOLOGY-MAPPER[/bold cyan]\n[italic white]Infrastructure Visualizer (Infra-Map)[/italic white]",
            border_style="blue"
        )

    @staticmethod
    def generate_tree(data):
        tree = Tree("\n[bold green]🌍 LocalStack Root[/bold green]")

        s3_group = tree.add("📂 [bold yellow]S3 Storage[/bold yellow]")
        if not data["s3"]:
            s3_group.add("[dim]No buckets found[/dim]")
        for bucket in data["s3"]:
            b_node = s3_group.add(f"📦 [bold]{bucket['name']}[/bold]")
            for trigger in bucket["triggers"]:
                b_node.add(f"[italic magenta]{trigger}[/italic magenta]")

        lmb_group = tree.add("⚡ [bold orange3]Compute (Lambda)[/bold orange3]")
        if not data["lambda"]:
            lmb_group.add("[dim]No functions found[/dim]")
        for l in data["lambda"]:
            lmb_group.add(f"λ {l['name']} [dim]({l['runtime']})[/dim]")

        sqs_group = tree.add("📨 [bold magenta]Messaging (SQS)[/bold magenta]")
        if not data["sqs"]:
            sqs_group.add("[dim]No queues found[/dim]")
        for q in data["sqs"]:
            sqs_group.add(f"📥 {q['name']}")

        return tree