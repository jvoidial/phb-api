import time

class TaskGenerator:
    def generate(self, state):
        tasks = []

        # simple safe heuristics
        if len(state.get("recent_events", [])) > 5:
            tasks.append("summarise_memory")

        if state.get("idle", True):
            tasks.append("self_check")

        return tasks
