class HealthScorer:
    def score(self, snapshot):
        score = 100

        if snapshot["tasks"] > 50:
            score -= 20

        if snapshot["memory_users"] > 100:
            score -= 10

        if snapshot["agents"] > 50:
            score -= 10

        return max(0, score)
