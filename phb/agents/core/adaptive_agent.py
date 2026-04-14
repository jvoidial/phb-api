class AdaptiveAgent:
    def __init__(self, memory):
        self.memory = memory
        self.personality_bias = 1.0

    def analyze_memory(self, user):
        mem = self.memory.read(user)

        # simple signal extraction
        if len(mem) > 5:
            self.personality_bias += 0.1
        else:
            self.personality_bias -= 0.05

        self.personality_bias = max(0.5, min(2.0, self.personality_bias))

        return mem

    def respond(self, user, msg):
        mem = self.analyze_memory(user)

        tone = "neutral"

        if self.personality_bias > 1.5:
            tone = "deep reflective"
        elif self.personality_bias < 0.8:
            tone = "concise"

        context = " | ".join([m["msg"] for m in mem[-3:]]) if mem else ""

        return {
            "response": f"[{tone}] {msg}",
            "context": context,
            "bias": self.personality_bias
        }
