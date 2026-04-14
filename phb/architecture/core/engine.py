from phb.architecture.core.graph import ArchitectureGraph
from phb.architecture.core.analyzer import ArchitectureAnalyzer
from phb.architecture.core.evolver import ArchitectureEvolver
from phb.architecture.core.simulator import ArchitectureSimulator
from phb.architecture.core.safety import SafetyController

class ArchitectureEngine:
    def __init__(self):
        self.graph = ArchitectureGraph()
        self.analyzer = ArchitectureAnalyzer()
        self.evolver = ArchitectureEvolver()
        self.sim = ArchitectureSimulator()
        self.safety = SafetyController()

    def evolve(self):
        snapshot = self.graph.snapshot()

        proposals = self.evolver.propose(snapshot)

        results = []

        for p in proposals:
            simulated = self.sim.simulate(snapshot, p)

            if self.safety.validate(snapshot, simulated):
                results.append(p)

        return results
