class MetaSelector:
    def select(self, simulations, resonance_map):
        best = None
        best_score = -1

        for sim in simulations:
            score = sim["score"]
            design = sim["design"]
            resonance = resonance_map.get(design, 0)

            final_score = (score * 0.6) + (resonance * 0.4)

            if final_score > best_score:
                best_score = final_score
                best = sim

        return {
            "selected": best,
            "score": best_score
        }
