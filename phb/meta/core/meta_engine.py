class MetaLearningEngine:
    def __init__(self):
        self.adjustments = {
            "memory_decay": 0.95,
            "reinforcement_strength": 1.0,
            "strategy_sensitivity": 1.0
        }

    def evaluate(self, before, after):
        improvement = after - before

        if improvement < 0:
            self.adjustments["reinforcement_strength"] *= 0.95

        if improvement > 0.2:
            self.adjustments["reinforcement_strength"] *= 1.05

        return self.adjustments
