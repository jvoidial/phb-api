from phb.meta.voxels.voxel import Voxel

class VoxelField:
    def __init__(self):
        self.grid = {}

    def set(self, key, value):
        if key not in self.grid:
            self.grid[key] = Voxel(value)
        else:
            self.grid[key].update(value)

    def state(self):
        return {
            k: {
                "energy": v.energy,
                "coherence": v.coherence
            }
            for k, v in self.grid.items()
        }
