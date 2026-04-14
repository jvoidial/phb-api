class StrategyScorer:
    def score(self, timeline):
        final_state = timeline[-1]

        health = final_state.get("health", 1.0)
        load = final_state.get("load", 0.0)
        nodes = final_state.get("nodes", 1)

        score = (health * 0.6) + (nodes * 0.2) - (load * 0.2)

        return score
