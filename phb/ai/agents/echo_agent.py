from phb.ai.agents.base_agent import BaseAgent

class EchoAgent(BaseAgent):
    def handle(self, event):
        msg = event.get("msg", "")
        if "echo" in msg:
            return f"[EchoAgent] {msg}"
        return None
