from phb.mesh.agents.base import Agent

class AnalyzerAgent(Agent):
    def run(self, event, board):
        msg = event.get("msg", "")
        if len(msg) > 20:
            return "📊 long input detected"
        return None
