from collections import defaultdict
from datetime import datetime

class WorldModel:
    """
    Lightweight predictive state model
    """

    def __init__(self):
        self.state = {
            "intent_patterns": defaultdict(int),
            "memory_growth_rate": [],
            "interaction_flow": []
        }

    def update(self, message, memory_count):
        self.state["intent_patterns"][message] += 1
        self.state["memory_growth_rate"].append(memory_count)

        self.state["interaction_flow"].append({
            "message": message,
            "time": datetime.utcnow().isoformat()
        })

    def predict_next_intent(self):
        if not self.state["intent_patterns"]:
            return ["unknown"]

        sorted_intents = sorted(
            self.state["intent_patterns"].items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [i[0] for i in sorted_intents[:3]]

    def predict_memory_trend(self):
        if len(self.state["memory_growth_rate"]) < 2:
            return "stable"

        growth = self.state["memory_growth_rate"]
        return "increasing" if growth[-1] > growth[0] else "stable"
