class ExecutionGuard:
    def allow(self, task):
        blocked = ["delete_kernel", "self_destruct"]
        return task not in blocked
