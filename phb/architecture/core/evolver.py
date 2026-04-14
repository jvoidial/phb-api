import copy

class ArchitectureEvolver:
    def propose(self, graph):
        proposals = []

        for node, data in graph["nodes"].items():
            if data["load"] > 0.7:
                proposals.append({
                    "action": "split_node",
                    "target": node
                })

        return proposals

    def apply(self, graph, proposal):
        new_graph = copy.deepcopy(graph)

        if proposal["action"] == "split_node":
            target = proposal["target"]
            new_graph["nodes"][target]["load"] *= 0.5

        return new_graph
