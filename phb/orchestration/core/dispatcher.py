class TaskDispatcher:
    def __init__(self, kernel):
        self.kernel = kernel

    def dispatch(self, task_type, payload):
        if task_type == "learn":
            return self.kernel.learn(payload.get("action"), payload.get("score", 0.5))

        if task_type == "plan":
            return self.kernel.generate_plan()

        if task_type == "consensus":
            return self.kernel.consensus_tick()

        if task_type == "upgrade":
            return self.kernel.run_upgrade_cycle()

        return "unknown task"
