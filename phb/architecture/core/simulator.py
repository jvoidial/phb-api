import copy

class ArchitectureSimulator:
    def simulate(self, graph, proposal):
        simulated = copy.deepcopy(graph)

        if proposal["action"] == "split_node":
            node = proposal["target"]
            simulated["nodes"][node]["load"] *= 0.5

        return simulated
