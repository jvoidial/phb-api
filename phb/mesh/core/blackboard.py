class Blackboard:
    def __init__(self):
        self.state = {}

    def write(self, key, value):
        self.state[key] = value

    def read(self, key, default=None):
        return self.state.get(key, default)

    def all(self):
        return self.state
