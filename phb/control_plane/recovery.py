import time

class RecoveryEngine:
    def __init__(self, kernel):
        self.kernel = kernel

    def heal(self):
        try:
            if not self.kernel.running:
                print("🔁 Recovery: restarting kernel")
                self.kernel.start()
        except Exception as e:
            print("⚠️ Recovery failed:", e)
