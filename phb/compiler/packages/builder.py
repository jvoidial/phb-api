class PackageBuilder:
    def build(self, patch, simulation, score):
        return {
            "upgrade": patch,
            "simulation": simulation,
            "score": score,
            "status": "ready_for_manual_review"
        }
