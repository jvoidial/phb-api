import time

class FailureDetector:
    def __init__(self, timeout=10):
        self.timeout = timeout

    def is_dead(self, node):
        return (time.time() - node.last_heartbeat) > self.timeout
