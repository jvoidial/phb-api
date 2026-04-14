class ArchitectureGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, name, load=0.0):
        self.nodes[name] = {"load": load}

    def add_edge(self, a, b):
        self.edges.append((a, b))

    def snapshot(self):
        return {
            "nodes": self.nodes,
            "edges": self.edges
        }
