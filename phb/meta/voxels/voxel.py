class Voxel:
    def __init__(self, value=0.0):
        self.energy = value
        self.coherence = 1.0
        self.decay = 0.01
        self.persistence = 1.0

    def update(self, signal):
        self.energy += signal
        self.energy *= (1 - self.decay)

        # coherence stabilizes strong signals
        if self.energy > 1.0:
            self.coherence += 0.01
        else:
            self.coherence -= 0.01

        self.coherence = max(0.0, min(1.0, self.coherence))
