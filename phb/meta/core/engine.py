from phb.meta.core.observer import LearningObserver
from phb.meta.core.meta_engine import MetaLearningEngine
from phb.meta.core.analyzer import PerformanceAnalyzer
from phb.meta.core.controller import SafeRefinementController

class MetaSystem:
    def __init__(self):
        self.observer = LearningObserver()
        self.meta = MetaLearningEngine()
        self.analyzer = PerformanceAnalyzer()
        self.controller = SafeRefinementController()

    def step(self, before, after, config):
        score = self.analyzer.score(before, after)

        self.observer.log(score, config)

        new_config = self.meta.evaluate(before, after)

        # safety clamp
        for k in new_config:
            new_config[k] = self.controller.clamp(new_config[k])

        return new_config
