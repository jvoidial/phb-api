class SafeRefinementController:
    def __init__(self):
        self.max_change = 0.1

    def clamp(self, value):
        if value > 1 + self.max_change:
            return 1 + self.max_change
        if value < 0.1:
            return 0.1
        return value
