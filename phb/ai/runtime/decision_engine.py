class DecisionEngine:
    def decide(self, agent_outputs, fallback):
        for output in agent_outputs:
            if output:
                return output
        return fallback
