class GlobalMemory:
    def __init__(self):
        self.store = {}

    def write(self, key, value, source="unknown"):
        if key not in self.store:
            self.store[key] = []

        self.store[key].append({
            "value": value,
            "source": source
        })

    def read(self, key):
        return self.store.get(key, [])
