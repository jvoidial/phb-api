from phb.orchestration.core.state import SystemState
from phb.orchestration.core.dispatcher import TaskDispatcher

class OrchestrationEngine:
    def __init__(self, kernel):
        self.kernel = kernel
        self.state = SystemState()
        self.dispatcher = TaskDispatcher(kernel)

    def tick(self):
        # system-wide coordination cycle

        health = 1.0

        try:
            self.kernel.consensus_tick()
        except:
            health -= 0.2

        try:
            self.kernel.planning_cycle()
        except:
            health -= 0.2

        self.state.update("health", health)

        return self.state.snapshot()

    def route(self, task_type, payload):
        return self.dispatcher.dispatch(task_type, payload)
