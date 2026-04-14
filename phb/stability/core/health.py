import time

class HealthMonitor:
    def report(self, kernel):
        return {
            "agents": len(kernel.mesh.agents),
            "memory_keys": len(kernel.board.all()),
            "uptime": time.time()
        }
