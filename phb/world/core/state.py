class WorldState:
    def __init__(self):
        self.state = {
            "health": 1.0,
            "load": 0.0,
            "events": [],
            "nodes": 1,
            "tasks": []
        }

    def update(self, key, value):
        self.state[key] = value

    def snapshot(self):
        return self.state
