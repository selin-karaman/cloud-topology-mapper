import boto3

class DiscoveryEngine:
    def __init__(self, endpoint_url="http://localhost:4566"):
        self.endpoint = endpoint_url
        self.session = boto3.Session(
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1"
        )

    def get_client(self, service_name):
        return self.session.client(service_name, endpoint_url=self.endpoint)

    def get_topology(self):
        topology = {
            "s3": self._scan_s3(),
            "lambda": self._scan_lambda(),
            "sqs": self._scan_sqs()
        }
        return topology

    def _scan_s3(self):
        client = self.get_client("s3")
        try:
            buckets = client.list_buckets()["Buckets"]
            results = []
            for b in buckets:
                notif = client.get_bucket_notification_configuration(Bucket=b["Name"])
                triggers = []
                if "LambdaFunctionConfigurations" in notif:
                    for lc in notif["LambdaFunctionConfigurations"]:
                        triggers.append(f"-> Lambda: {lc['LambdaFunctionArn'].split(':')[-1]}")
                
                results.append({"name": b["Name"], "triggers": triggers})
            return results
        except: return []

    def _scan_lambda(self):
        client = self.get_client("lambda")
        try:
            funcs = client.list_functions()["Functions"]
            return [{"name": f["FunctionName"], "runtime": f["Runtime"]} for f in funcs]
        except: return []

    def _scan_sqs(self):
        client = self.get_client("sqs")
        try:
            urls = client.list_queues().get("QueueUrls", [])
            return [{"name": url.split("/")[-1]} for url in urls]
        except: return []