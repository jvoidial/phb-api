from phb.orchestration.kernel import OrchestrationKernel

class SystemOrchestrator:
    def __init__(self):
        self.kernel = OrchestrationKernel()

    def ingest(self, subsystem, action, priority=1):
        self.kernel.submit({
            "subsystem": subsystem,
            "action": action,
            "priority": priority
        })

    def tick(self):
        self.kernel.prioritize()
        return self.kernel.dispatch()
