class SwarmOptimizer:
    def __init__(self, consensus):
        self.consensus = consensus
        self.performance_log = {}

    def record_result(self, node_id, decision, success):
        if node_id not in self.performance_log:
            self.performance_log[node_id] = []

        self.performance_log[node_id].append(success)

    def update_weights(self):
        for node_id, history in self.performance_log.items():
            score = sum(history) / len(history)

            # adaptive weighting
            if score > 0.7:
                self.consensus.set_weight(node_id, 1.5)
            elif score < 0.4:
                self.consensus.set_weight(node_id, 0.5)
            else:
                self.consensus.set_weight(node_id, 1.0)
