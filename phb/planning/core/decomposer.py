class TaskDecomposer:
    def breakdown(self, goal):
        # simple deterministic decomposition
        return [
            f"analyze {goal}",
            f"plan steps for {goal}",
            f"execute {goal}",
            f"verify {goal}"
        ]
