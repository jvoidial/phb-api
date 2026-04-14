import uuid
import math

class MemoryGraphAI:
    def __init__(self):
        self.nodes = []

    def add(self, text, tags=None, weight=0.5):
        node = {
            "id": str(uuid.uuid4()),
            "text": text,
            "tags": tags or [],
            "weight": weight
        }
        self.nodes.append(node)
        return node

    def recall(self, keyword):
        results = []
        for n in self.nodes:
            score = 0
            if keyword.lower() in n["text"].lower():
                score += 1
            score += n["weight"]
            if score > 1:
                results.append(n)
        return results[-5:]  # most relevant recent memories
