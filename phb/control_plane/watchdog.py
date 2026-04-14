import time
import threading

class Watchdog:
    def __init__(self, kernel, interval=3):
        self.kernel = kernel
        self.interval = interval
        self.last_beat = time.time()
        self.running = False

    def beat(self):
        self.last_beat = time.time()

    def start(self):
        print("🛡️ Watchdog ACTIVE")
        self.running = True
        threading.Thread(target=self.monitor, daemon=True).start()

    def monitor(self):
        while self.running:
            time.sleep(self.interval)

            if time.time() - self.last_beat > self.interval * 2:
                print("⚠️ Kernel heartbeat lost → restarting loop")
                try:
                    self.kernel.stop()
                except:
                    pass
                self.kernel.start()
                self.last_beat = time.time()
