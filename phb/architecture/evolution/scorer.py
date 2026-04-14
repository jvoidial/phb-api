class ArchitectureScorer:
    def score(self, simulated_state):
        stability = simulated_state.get("memory_stability", 0.5)
        latency = simulated_state.get("event_latency", 1.0)

        return {
            "stability_score": stability,
            "performance_score": 1 / (latency + 0.1),
            "risk_score": 1 - stability
        }
