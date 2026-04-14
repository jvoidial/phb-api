class BehaviorModel:
    def __init__(self):
        self.weights = {}

    def update(self, action, score):
        if action not in self.weights:
            self.weights[action] = 0.5

        # reinforcement learning style update
        self.weights[action] = (
            self.weights[action] * 0.8 + score * 0.2
        )

    def choose(self):
        if not self.weights:
            return None

        return max(self.weights, key=self.weights.get)
