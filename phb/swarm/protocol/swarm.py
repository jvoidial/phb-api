class SwarmProtocol:
    def __init__(self, registry, consensus):
        self.registry = registry
        self.consensus = consensus

    def broadcast(self, task):
        votes = []

        for node_id, node in self.registry.nodes.items():
            decision = node.receive_task(task)
            votes.append(self.consensus.vote(node_id, decision))

        return self.consensus.aggregate(votes)
