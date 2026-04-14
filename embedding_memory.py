import math
import time
from collections import defaultdict

# -----------------------------
# SIMPLE LOCAL EMBEDDING BRAIN
# (lightweight semantic approximation)
# -----------------------------

class EmbeddingMemory:
    def __init__(self):
        self.memories = []

    # --- pseudo embedding ---
    # converts text → weighted token map
    def embed(self, text):
        vec = defaultdict(float)
        words = text.lower().split()

        for i, w in enumerate(words):
            vec[w] += 1.0
            vec[w[:3]] += 0.5  # sub-word signal

        return vec

    # cosine similarity between sparse vectors
    def similarity(self, v1, v2):
        dot = 0.0
        mag1 = 0.0
        mag2 = 0.0

        for k in set(v1.keys()).union(v2.keys()):
            a = v1.get(k, 0.0)
            b = v2.get(k, 0.0)
            dot += a * b
            mag1 += a * a
            mag2 += b * b

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot / (math.sqrt(mag1) * math.sqrt(mag2))

    def add(self, text, tags=None, weight=0.5):
        self.memories.append({
            "text": text,
            "vector": self.embed(text),
            "tags": tags or [],
            "weight": weight,
            "time": time.time()
        })

    def recall(self, query, top_k=3):
        q_vec = self.embed(query)

        scored = []

        for m in self.memories:
            sim = self.similarity(q_vec, m["vector"])

            score = sim * 0.8 + m["weight"] * 0.2

            scored.append((score, m))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [m for _, m in scored[:top_k]]


# GLOBAL MEMORY BRAIN (IMPORTANT)
GLOBAL_EMBED_MEMORY = EmbeddingMemory()
