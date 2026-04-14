class Arbitrator:
    def decide(self, outputs, fallback):
        for o in outputs:
            if o:
                return o
        return fallback
