from phb.strategy.core.memory import StrategicMemory
from phb.strategy.core.timeline import TimelineEngine
from phb.strategy.core.scorer import StrategyScorer

class StrategyEngine:
    def __init__(self):
        self.memory = StrategicMemory()
        self.timeline = TimelineEngine()
        self.scorer = StrategyScorer()

    def evaluate(self, world_model, action_sets):
        timelines = self.timeline.build(world_model, action_sets)

        scored = []

        for t in timelines:
            score = self.scorer.score(t)
            scored.append((t, score))

        best = max(scored, key=lambda x: x[1])

        self.memory.record(best[0], best[1])

        return {
            "best_timeline": best[0],
            "score": best[1],
            "all_scores": scored
        }
