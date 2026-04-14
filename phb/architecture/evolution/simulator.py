import copy

class ArchitectureSimulator:
    def simulate(self, state, proposal):
        simulated = copy.deepcopy(state)

        if proposal["name"] == "optimize_event_routing":
            simulated["event_latency"] = 0.5

        if proposal["name"] == "enhance_memory_coherence":
            simulated["memory_stability"] = 0.9

        return simulated
