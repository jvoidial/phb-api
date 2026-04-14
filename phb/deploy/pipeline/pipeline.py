class DeploymentPipeline:
    def __init__(self):
        self.stages = {
            "dev": [],
            "staging": [],
            "candidate": [],
            "approved": []
        }

    def submit(self, design):
        self.stages["dev"].append(design)

    def promote(self, design, stage):
        if design in self.stages["dev"]:
            self.stages["dev"].remove(design)
            self.stages[stage].append(design)

    def get_best_candidate(self):
        candidates = self.stages["candidate"]
        return max(candidates, key=lambda x: x.get("score", 0), default=None)
