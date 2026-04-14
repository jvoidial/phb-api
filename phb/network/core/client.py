import requests

class NodeClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def health(self):
        return requests.get(f"{self.base_url}/health").json()

    def heartbeat(self):
        return requests.post(f"{self.base_url}/heartbeat").json()

    def send_task(self, msg):
        return requests.post(
            f"{self.base_url}/task",
            json={"msg": msg}
        ).json()
