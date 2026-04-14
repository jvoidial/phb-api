class EvolutionEngine:
    def propose(self, analysis):
        proposals = []

        if "cluster_routing" in analysis.get("bottlenecks", []):
            proposals.append("optimize_task_router_v2")

        if "node_sync_latency" in analysis.get("weak_points", []):
            proposals.append("introduce_fast_sync_layer")

        return proposals
