class StrategySelector:
    def choose(self, timelines):
        best = None

        for t in timelines:
            if best is None or t.score > best.score:
                best = t

        return best
