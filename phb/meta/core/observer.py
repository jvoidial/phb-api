class LearningObserver:
    def __init__(self):
        self.records = []

    def log(self, system_metric, learning_config):
        self.records.append({
            "metric": system_metric,
            "config": learning_config
        })

    def get_history(self):
        return self.records
