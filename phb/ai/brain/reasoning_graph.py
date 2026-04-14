import time

class ReasoningGraph:
    def __init__(self):
        self.nodes = []

    def add(self, input_text, decision, output):
        self.nodes.append({
            "t": time.time(),
            "input": input_text,
            "decision": decision,
            "output": output
        })

    def recent(self, n=10):
        return self.nodes[-n:]
