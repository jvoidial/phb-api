class LeaderElection:
    def __init__(self):
        self.leader = None

    def elect(self, nodes):
        alive = [n for n in nodes if n.is_alive()]

        if not alive:
            self.leader = None
            return None

        # simplest deterministic election: first alive node
        self.leader = alive[0].node_id
        return self.leader

    def get_leader(self):
        return self.leader
