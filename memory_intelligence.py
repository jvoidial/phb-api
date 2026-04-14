import time
import math

class MemoryIntelligence:
    def __init__(self):
        self.memories = []

    def add(self, text, tags=None, weight=0.5):
        self.memories.append({
            "text": text,
            "tags": tags or [],
            "weight": weight,
            "time": time.time()
        })

    def _score(self, query, memory):
        score = 0.0

        q = set(query.lower().split())
        m = set(memory["text"].lower().split())

        score += len(q & m) * 0.6
        score += memory["weight"] * 0.4

        age = time.time() - memory["time"]
        score *= math.exp(-age / 3600)

        return score

    def recall(self, query, top_k=3):
        scored = []

        for m in self.memories:
            s = self._score(query, m)
            if s > 0:
                scored.append((s, m))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored[:top_k]]


# 🔥 GLOBAL SINGLETON (IMPORTANT FIX)
GLOBAL_MEMORY = MemoryIntelligence()
