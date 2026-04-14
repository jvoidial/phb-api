import json
import time
import os

class Checkpoint:
    def __init__(self, path="state/checkpoint.json"):
        self.path = path
        os.makedirs("state", exist_ok=True)

    def save(self, data):
        data["timestamp"] = time.time()
        with open(self.path, "w") as f:
            json.dump(data, f)

    def load(self):
        if not os.path.exists(self.path):
            return None
        with open(self.path) as f:
            return json.load(f)
