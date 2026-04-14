class ExperienceTracker:
    def __init__(self):
        self.log = []

    def record(self, action, success_score=0.5):
        self.log.append({
            "action": action,
            "score": success_score
        })

    def get_all(self):
        return self.log
