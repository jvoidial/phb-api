import copy

class Simulator:
    def simulate(self, state, action):
        # shallow deterministic simulation model

        new_state = copy.deepcopy(state)

        if action == "increase_load":
            new_state["load"] += 0.2

        elif action == "reduce_load":
            new_state["load"] = max(0.0, new_state["load"] - 0.2)

        elif action == "spawn_node":
            new_state["nodes"] += 1

        elif action == "system_stress":
            new_state["health"] -= 0.3

        return new_state
