class SwarmMetrics:
    def __init__(self):
        self.data = []

    def log(self, consensus_result, expected_result):
        self.data.append({
            "consensus": consensus_result,
            "expected": expected_result,
            "match": consensus_result == expected_result
        })

    def accuracy(self):
        if not self.data:
            return 0.0

        correct = sum(1 for d in self.data if d["match"])
        return correct / len(self.data)
