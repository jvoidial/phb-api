# PHB STABLE MEMORY KERNEL (FAISS-FREE)

class SimpleVectorMemory:
    def __init__(self):
        self.vectors = []

    def embed(self, text):
        vec = {}
        for w in text.lower().split():
            vec[w] = vec.get(w, 0) + 1.0
        return vec

    def similarity(self, a, b):
        score = 0.0
        for k in a:
            if k in b:
                score += a[k] * b[k]
        return score

    def store(self, text):
        vec = self.embed(text)
        self.vectors.append({"text": text, "vec": vec})
        return vec

    def search(self, text):
        query = self.embed(text)

        scored = []
        for item in self.vectors:
            s = self.similarity(query, item["vec"])
            scored.append((s, item["text"]))

        scored.sort(reverse=True, key=lambda x: x[0])
        return scored[:5]


KERNEL = SimpleVectorMemory()
