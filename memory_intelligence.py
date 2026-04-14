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

    # simple similarity scoring (lightweight, no embeddings needed)
    def _score(self, query, memory):
        score = 0.0

        q_words = set(query.lower().split())
        m_words = set(memory["text"].lower().split())

        overlap = len(q_words & m_words)
        score += overlap * 0.6

        score += memory["weight"] * 0.4

        age = time.time() - memory["time"]
        decay = math.exp(-age / 3600)  # 1-hour decay curve
        score *= decay

        return score

    def recall(self, query, top_k=3):
        scored = []

        for m in self.memories:
            s = self._score(query, m)
            if s > 0:
                scored.append((s, m))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [m for s, m in scored[:top_k]]
