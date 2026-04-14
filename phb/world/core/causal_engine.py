import copy

class CausalEngine:
    def apply_event(self, graph, event):
        new_graph = copy.deepcopy(graph)

        target = event.get("target")
        impact = event.get("impact", 0.1)

        if target in new_graph["nodes"]:
            new_graph["nodes"][target]["load"] = \
                new_graph["nodes"][target].get("load", 0) + impact

        return new_graph
