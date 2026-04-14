class ClusterSync:
    def __init__(self, control_plane):
        self.cp = control_plane

    def snapshot(self):
        return {
            "nodes": [
                {
                    "id": n.node_id,
                    "alive": n.is_alive()
                }
                for n in self.cp.nodes.values()
            ]
        }
