import time
import threading

class Watchdog:
    def __init__(self, kernel):
        self.kernel = kernel
        self.running = False
        self.last_tick = time.time()

    def kick(self):
        self.last_tick = time.time()

    def start(self):
        print("🛡️ Watchdog ACTIVE")
        self.running = True
        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while self.running:
            time.sleep(2)
            if time.time() - self.last_tick > 10:
                print("⚠️ Watchdog: system stall detected → restarting kernel loop")
                try:
                    self.kernel.restart_loop()
                except Exception as e:
                    print("❌ Watchdog recovery failed:", e)
