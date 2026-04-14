import copy

class PredictionEngine:
    def simulate(self, graph, steps=3):
        simulations = []

        current = copy.deepcopy(graph)

        for _ in range(steps):
            for node in current["nodes"]:
                load = current["nodes"][node].get("load", 0)
                current["nodes"][node]["load"] = load * 1.01

            simulations.append(copy.deepcopy(current))

        return simulations
