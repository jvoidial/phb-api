class DesignRegistry:
    def __init__(self):
        self.history = []

    def store(self, result):
        self.history.append(result)

    def best(self):
        return max(self.history, key=lambda x: x["score"], default=None)
