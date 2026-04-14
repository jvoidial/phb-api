class ArchitectureAnalyzer:
    def find_bottlenecks(self, graph):
        return [
            node for node, data in graph["nodes"].items()
            if data["load"] > 0.7
        ]
