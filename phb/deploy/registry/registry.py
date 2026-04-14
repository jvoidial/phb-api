class DeploymentRegistry:
    def __init__(self):
        self.history = []

    def record(self, design, stage):
        self.history.append({
            "design": design,
            "stage": stage
        })

    def rollback(self):
        return self.history[-1] if self.history else None
