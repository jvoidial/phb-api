from phb.distributed.core.node import Node

class ControlPlane:
    def __init__(self):
        self.nodes = {}

    def register_node(self, node_id, address):
        print(f"🌐 Registering node: {node_id}")
        self.nodes[node_id] = Node(node_id, address)

    def heartbeat(self, node_id):
        if node_id in self.nodes:
            self.nodes[node_id].heartbeat()

    def active_nodes(self):
        return [n for n in self.nodes.values() if n.is_alive()]

    def get_node(self, node_id):
        return self.nodes.get(node_id)
