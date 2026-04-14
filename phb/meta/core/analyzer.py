class PerformanceAnalyzer:
    def score(self, predicted, actual):
        return 1.0 - abs(predicted - actual)
