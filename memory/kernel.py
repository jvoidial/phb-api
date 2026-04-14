import json, os, time

FILE = "memory_store.json"

class MemoryKernel:
    def __init__(self):
        if not os.path.exists(FILE):
            with open(FILE, "w") as f:
                json.dump([], f)

    def load(self):
        return json.load(open(FILE))

    def save(self, data):
        json.dump(data, open(FILE, "w"), indent=2)

    def add(self, user_id, text):
        data = self.load()
        data.append({
            "user_id": user_id,
            "text": text,
            "time": time.time()
        })
        self.save(data)

    def search(self, user_id, query):
        data = self.load()
        return [
            x for x in data
            if x["user_id"] == user_id and query.lower() in x["text"].lower()
        ]

KERNEL = MemoryKernel()
