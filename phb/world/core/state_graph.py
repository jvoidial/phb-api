class WorldStateGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node_id, state=None):
        self.nodes[node_id] = state or {}

    def add_edge(self, a, b, relation="causal"):
        self.edges.append((a, b, relation))

    def snapshot(self):
        return {
            "nodes": self.nodes,
            "edges": self.edges
        }
