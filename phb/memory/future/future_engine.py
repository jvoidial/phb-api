from phb.memory.future.engine import FutureEngine
from phb.memory.future.scorer import StrategyScorer
from phb.memory.future.selector import StrategySelector

class StrategicFutureEngine:
    def __init__(self):
        self.engine = FutureEngine()
        self.scorer = StrategyScorer()
        self.selector = StrategySelector()

    def evaluate(self, state):
        timelines = self.engine.generate(state)

        for t in timelines:
            self.scorer.score(t)

        best = self.selector.choose(timelines)

        return {
            "best_timeline": best.state,
            "score": best.score,
            "alternatives": [t.state for t in timelines]
        }
