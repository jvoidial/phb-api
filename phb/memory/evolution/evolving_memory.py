import time

class EvolvingMemory:
    def __init__(self, decay_rate=0.01):
        self.data = {}
        self.decay_rate = decay_rate

    def write(self, user, message):
        entry = {
            "msg": message,
            "score": 1.0,
            "time": time.time()
        }

        self.data.setdefault(user, []).append(entry)

    def decay(self):
        for user, items in self.data.items():
            for item in items:
                age = time.time() - item["time"]
                item["score"] -= age * self.decay_rate

        # remove dead memory
        for user in self.data:
            self.data[user] = [m for m in self.data[user] if m["score"] > 0]

    def read(self, user, limit=5):
        self.decay()

        memories = self.data.get(user, [])
        memories = sorted(memories, key=lambda x: x["score"], reverse=True)

        return memories[:limit]

    def reinforce(self, user, message):
        for m in self.data.get(user, []):
            if m["msg"] == message:
                m["score"] += 0.5
