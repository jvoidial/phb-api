class ConsensusEngine:
    def __init__(self):
        self.weights = {}

    def set_weight(self, node_id, weight):
        self.weights[node_id] = weight

    def vote(self, node_id, decision):
        weight = self.weights.get(node_id, 1.0)
        return {"decision": decision, "weight": weight}

    def aggregate(self, votes):
        score = {}

        for v in votes:
            d = v["decision"]
            w = v["weight"]
            score[d] = score.get(d, 0) + w

        return max(score.items(), key=lambda x: x[1])[0]
