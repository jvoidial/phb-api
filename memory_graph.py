import json
import time
import uuid

class MemoryGraph:
    def __init__(self):
        self.nodes = []

    def add(self, text, tags=None, weight=0.5):
        node = {
            "id": str(uuid.uuid4()),
            "text": text,
            "tags": tags or [],
            "weight": weight,
            "time": time.time(),
            "links": []
        }
        self.nodes.append(node)
        self._link_latest(node)
        return node

    def _link_latest(self, new_node):
        if len(self.nodes) > 1:
            new_node["links"].append(self.nodes[-2]["id"])

    def search(self, keyword):
        return [
            n for n in self.nodes
            if keyword.lower() in n["text"].lower()
        ]

    def export(self):
        return self.nodes
