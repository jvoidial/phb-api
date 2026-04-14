import time

class SelfHeal:
    def __init__(self, kernel):
        self.kernel = kernel

    def check(self):
        try:
            if not self.kernel.running:
                print("⚠️ Kernel down → restarting")
                self.kernel.start()
        except Exception as e:
            print("⚠️ Self-heal error:", e)

    def loop(self):
        while True:
            self.check()
            time.sleep(5)
