class PriorityEngine:
    def __init__(self):
        self.priority_map = {
            "echo": 1,
            "analyzer": 2
        }

    def rank(self, outputs):
        # outputs = [(agent, result)]
        outputs.sort(key=lambda x: self.priority_map.get(x[0], 0), reverse=True)
        return outputs
