import time

class Node:
    def __init__(self, node_id, address):
        self.node_id = node_id
        self.address = address
        self.last_heartbeat = time.time()
        self.status = "active"

    def heartbeat(self):
        self.last_heartbeat = time.time()
        self.status = "active"

    def is_alive(self):
        return (time.time() - self.last_heartbeat) < 10
