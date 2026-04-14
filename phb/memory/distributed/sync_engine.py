import requests

class SyncEngine:
    def __init__(self, cluster):
        self.cluster = cluster

    def sync_to_node(self, node, memory_packet):
        try:
            return node.send_task("sync", memory_packet)
        except:
            return None

    def broadcast_memory(self, packet):
        results = {}

        for name, node in self.cluster.nodes.items():
            try:
                results[name] = node.send_task("memory_sync", packet)
            except:
                results[name] = "failed"

        return results
