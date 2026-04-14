from phb.consensus.core.failure_detector import FailureDetector
from phb.consensus.core.leader_election import LeaderElection
from phb.consensus.core.state import ClusterState

class ConsensusEngine:
    def __init__(self, control_plane):
        self.cp = control_plane
        self.detector = FailureDetector()
        self.leader_election = LeaderElection()
        self.state = ClusterState()

    def tick(self):
        nodes = list(self.cp.nodes.values())

        # mark failures implicitly via detector
        alive_nodes = [n for n in nodes if not self.detector.is_dead(n)]

        # leader election
        leader = self.leader_election.elect(alive_nodes)

        # sync state from leader
        if leader:
            self.state.update("leader", leader)

        return {
            "leader": leader,
            "alive_nodes": len(alive_nodes),
            "total_nodes": len(nodes)
        }
