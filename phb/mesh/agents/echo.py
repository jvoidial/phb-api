from phb.mesh.agents.base import Agent

class EchoAgent(Agent):
    def run(self, event, board):
        msg = event.get("msg", "")
        if "echo" in msg:
            return f"[Echo] {msg}"
        return None
