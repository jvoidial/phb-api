class RealityExecutionGateway:
    def __init__(self):
        self.adapters = {}

    def register(self, name, adapter):
        self.adapters[name] = adapter

    def execute(self, intent):
        adapter = self.adapters.get(intent["target"])

        if not adapter:
            return {"status": "rejected", "reason": "no adapter"}

        # safety gate
        if intent.get("risk", 1.0) > 0.7:
            return {"status": "blocked", "reason": "high risk"}

        return adapter.run(intent)
