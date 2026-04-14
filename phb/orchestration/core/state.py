class SystemState:
    def __init__(self):
        self.state = {
            "health": 1.0,
            "mode": "SAFE",
            "nodes": 1
        }

    def update(self, key, value):
        self.state[key] = value

    def snapshot(self):
        return self.state
