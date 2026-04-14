class DesignSimulator:
    def simulate(self, design):
        score = 0.0

        if "routing" in design["change"]:
            score += 0.8
        if "memory" in design["change"]:
            score += 0.7
        if "cluster" in design["change"]:
            score += 0.9

        return {
            "version": design["version"],
            "score": score,
            "safe": score < 1.0
        }
