from phb.architecture.evolution.proposer import ArchitectureProposer
from phb.architecture.evolution.simulator import ArchitectureSimulator
from phb.architecture.evolution.scorer import ArchitectureScorer

class ArchitectureEvolutionEngine:
    def __init__(self):
        self.proposer = ArchitectureProposer()
        self.simulator = ArchitectureSimulator()
        self.scorer = ArchitectureScorer()

    def evaluate(self, state):
        proposals = self.proposer.propose(state)

        results = []

        for p in proposals:
            sim = self.simulator.simulate(state, p)
            score = self.scorer.score(sim)

            results.append({
                "proposal": p,
                "score": score
            })

        return results
