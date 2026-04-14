class Timeline:
    def __init__(self, state, weight=1.0):
        self.state = state
        self.weight = weight
        self.score = 0.0

    def update_score(self, value):
        self.score += value
