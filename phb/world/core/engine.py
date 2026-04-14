from phb.world.core.state_graph import WorldStateGraph
from phb.world.core.causal_engine import CausalEngine
from phb.world.core.predictor import PredictionEngine
from phb.world.core.diff import StateDiff

class WorldEngine:
    def __init__(self):
        self.graph = WorldStateGraph()
        self.causal = CausalEngine()
        self.predictor = PredictionEngine()
        self.diff = StateDiff()

    def tick(self, event):
        before = self.graph.snapshot()

        after_graph = self.causal.apply_event(before, event)

        predictions = self.predictor.simulate(after_graph)

        return {
            "before": before,
            "after": after_graph,
            "predictions": predictions,
            "diff": self.diff.compare(before, after_graph)
        }
