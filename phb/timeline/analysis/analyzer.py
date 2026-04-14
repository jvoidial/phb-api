class TimelineAnalyzer:
    def rank(self, simulations):
        return sorted(
            simulations,
            key=lambda x: x["score"],
            reverse=True
        )

    def best(self, simulations):
        ranked = self.rank(simulations)
        return ranked[0] if ranked else None
