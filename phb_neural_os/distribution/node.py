class PHBNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.peers = []

    def connect(self, peer):
        self.peers.append(peer)
