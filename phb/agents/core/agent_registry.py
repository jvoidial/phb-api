from phb.agents.core.adaptive_agent import AdaptiveAgent

class AgentRegistry:
    def __init__(self, memory):
        self.memory = memory
        self.agents = {}

    def get(self, name):
        if name not in self.agents:
            self.agents[name] = AdaptiveAgent(self.memory)
        return self.agents[name]
