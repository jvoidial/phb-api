import copy

class TimelineEngine:
    def build(self, world_model, actions):
        timelines = []

        for action in actions:
            state = copy.deepcopy(world_model)

            path = [state]

            for a in action:
                state = self.simulate_step(state, a)
                path.append(copy.deepcopy(state))

            timelines.append(path)

        return timelines

    def simulate_step(self, state, action):
        if action == "increase_load":
            state["load"] += 0.2

        if action == "reduce_load":
            state["load"] = max(0.0, state["load"] - 0.2)

        if action == "spawn_node":
            state["nodes"] += 1

        return state
