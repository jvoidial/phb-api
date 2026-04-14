class StrategyScorer:
    def score(self, timeline):
        total_load = sum(
            node.get("load", 0)
            for node in timeline.state.get("nodes", {}).values()
        )

        timeline.score = 1 / (1 + total_load)
        return timeline.score
