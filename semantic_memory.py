import math
import time
from collections import defaultdict

class SemanticMemory:
    def __init__(self):
        self.memories = []

    def embed(self, text):
        vec = defaultdict(float)
        words = text.lower().split()

        for w in words:
            vec[w] += 1.0
            vec[w[:3]] += 0.3  # weak semantic compression

        return vec

    def cosine(self, a, b):
        dot = 0
        ma = 0
        mb = 0

        keys = set(a.keys()) | set(b.keys())

        for k in keys:
            x = a.get(k, 0)
            y = b.get(k, 0)
            dot += x * y
            ma += x * x
            mb += y * y

        if ma == 0 or mb == 0:
            return 0

        return dot / (math.sqrt(ma) * math.sqrt(mb))

    def store(self, text, mood="neutral"):
        self.memories.append({
            "text": text,
            "vector": self.embed(text),
            "mood": mood,
            "weight": 1.0,
            "time": time.time()
        })

    def recall(self, query, top_k=5):
        qv = self.embed(query)

        scored = []
        for m in self.memories:
            score = self.cosine(qv, m["vector"]) * m["weight"]
            scored.append((score, m))

        scored.sort(reverse=True, key=lambda x: x[0])
        return [m for _, m in scored[:top_k]]

    def decay(self):
        for m in self.memories:
            age = time.time() - m["time"]
            m["weight"] *= max(0.5, 1.0 - age / 100000)
