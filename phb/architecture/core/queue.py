class UpgradeQueue:
    def __init__(self):
        self.queue = []

    def add(self, patch):
        self.queue.append(patch)

    def next(self):
        return self.queue.pop(0) if self.queue else None
