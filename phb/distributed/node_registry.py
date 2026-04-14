class NodeRegistry:
    def __init__(self):
        self.nodes = {}

    def register(self, name, node):
        print(f"🧩 Node registered: {name}")
        self.nodes[name] = node

    def get(self, name):
        return self.nodes.get(name)

    def all(self):
        return list(self.nodes.keys())
