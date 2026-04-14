from phb.network.core.client import NodeClient

class Cluster:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name, url):
        self.nodes[name] = NodeClient(url)

    def broadcast_health(self):
        return {n: c.health() for n, c in self.nodes.items()}

    def send_task(self, node, msg):
        return self.nodes[node].send_task(msg)
