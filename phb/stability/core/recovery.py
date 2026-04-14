class RecoveryEngine:
    def __init__(self, checkpoint):
        self.checkpoint = checkpoint

    def restore(self):
        state = self.checkpoint.load()
        if not state:
            print("ℹ️ No checkpoint found")
            return None

        print("♻️ Restoring system state...")
        return state
