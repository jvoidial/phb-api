import time
import json
import os
import math

MEM_FILE = "phb_memory.json"

def load():
    if os.path.exists(MEM_FILE):
        with open(MEM_FILE, "r") as f:
            return json.load(f)
    return []

def save(memories):
    with open(MEM_FILE, "w") as f:
        json.dump(memories, f)

class MemoryIntelligence:
    def __init__(self):
        self.memories = load()

    def add(self, text, tags=None, weight=0.5):
        self.memories.append({
            "text": text,
            "tags": tags or [],
            "weight": weight,
            "time": time.time()
        })
        save(self.memories)

    def _score(self, query, memory):
        q = set(query.lower().split())
        m = set(memory["text"].lower().split())

        score = len(q & m) * 0.6
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

# global instance
GLOBAL_MEMORY = MemoryIntelligence()
