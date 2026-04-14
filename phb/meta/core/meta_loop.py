import time
from phb.meta.core.introspector import Introspector
from phb.meta.core.scoring import HealthScorer
from phb.meta.core.improver import Improver

class MetaLoop:
    def __init__(self, kernel):
        self.kernel = kernel
        self.introspector = Introspector(kernel)
        self.scorer = HealthScorer()
        self.improver = Improver()
        self.running = False

    def start(self):
        self.running = True
        print("🧠 PHB v3.18 META LOOP ACTIVE")

        while self.running:
            snapshot = self.introspector.snapshot()
            score = self.scorer.score(snapshot)
            suggestions = self.improver.suggest(snapshot, score)

            print("📊 SYSTEM SCORE:", score)
            print("🧠 SUGGESTIONS:", suggestions)

            time.sleep(5)
