class StrategicMemory:
    def __init__(self):
        self.history = []
        self.success_patterns = []
        self.failure_patterns = []

    def record(self, strategy, outcome_score):
        self.history.append((strategy, outcome_score))

        if outcome_score > 0.7:
            self.success_patterns.append(strategy)
        elif outcome_score < 0.3:
            self.failure_patterns.append(strategy)

    def get_success_patterns(self):
        return self.success_patterns

    def get_failure_patterns(self):
        return self.failure_patterns
