class LocalMemory:
    def __init__(self, node_id):
        self.node_id = node_id
        self.memory = {}
        self.bias = {
            "recency_weight": 0.7,
            "trust_weight": 0.3
        }

    def write(self, key, value):
        self.memory[key] = value

    def read(self, key):
        return self.memory.get(key)
