import copy
from phb.memory.future.timeline import Timeline

class FutureEngine:
    def __init__(self):
        self.timelines = []

    def generate(self, state, branches=3):
        self.timelines = []

        for i in range(branches):
            new_state = copy.deepcopy(state)

            # simulate divergence
            for node in new_state.get("nodes", {}):
                new_state["nodes"][node]["load"] *= (1 + (i * 0.05))

            self.timelines.append(Timeline(new_state, weight=1.0 / (i + 1)))

        return self.timelines
