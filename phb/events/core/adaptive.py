import time

class AdaptiveSignalLayer:
    def __init__(self):
        self.signal_strength = {}
        self.decay_rate = 0.95

    def reinforce(self, event_type):
        self.signal_strength[event_type] = (
            self.signal_strength.get(event_type, 0.5) + 0.1
        )

    def decay(self):
        for k in self.signal_strength:
            self.signal_strength[k] *= self.decay_rate

    def get_strength(self, event_type):
        return self.signal_strength.get(event_type, 0.5)
