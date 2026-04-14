class ReasoningAgent:

    def plan(self, message, context, state):
        return {
            "steps": [
                "interpret emotional state",
                "check memory context",
                "generate response"
            ]
        }

    def respond(self, message, context, mood, plan):

        base = "I understand."

        if mood == "soft":
            base = "I’m here with you."

        if context:
            base += " This feels familiar."

        return base
