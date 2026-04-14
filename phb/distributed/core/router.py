class TaskRouter:
    def __init__(self, control_plane):
        self.cp = control_plane

    def route(self, task):
        nodes = self.cp.active_nodes()

        if not nodes:
            return "local"

        # simple routing: pick first active node
        return nodes[0].node_id
