from phb.meta.voxels.field import VoxelField

class MetaLearningEngine:
    def __init__(self):
        self.field = VoxelField()

    def observe(self, key, signal):
        self.field.set(key, signal)

    def refine(self):
        state = self.field.state()

        adjustments = {}

        for k, v in state.items():
            if v["coherence"] < 0.3:
                adjustments[k] = "decay_increase"
            elif v["coherence"] > 0.8:
                adjustments[k] = "reinforce"

        return adjustments
