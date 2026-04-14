import time

class Introspector:
    def __init__(self, kernel):
        self.kernel = kernel

    def snapshot(self):
        return {
            "time": time.time(),
            "memory_users": len(getattr(self.kernel.memory, "data", {})),
            "agents": len(getattr(self.kernel.agents, "agents", {})),
            "tasks": getattr(self.kernel.orchestrator.scheduler, "size", lambda: 0)()
        }
