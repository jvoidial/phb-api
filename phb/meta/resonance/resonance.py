class ResonanceEngine:
    def compute(self, simulations):
        scores = {}

        for sim in simulations:
            design = sim["design"]

            # Simple coherence model (frequency = alignment across sims)
            base = sim["score"]
            stability = sim.get("stability", 0.5)

            resonance = base * 0.7 + stability * 0.3

            scores[design] = resonance

        return scores
