import time
import threading

class CognitionLoop:
    def __init__(self, kernel):
        self.kernel = kernel
        self.running = False

    def start(self):
        print("🧠 PHB v3.10 AUTONOMOUS LOOP STARTING")
        self.running = True
        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while self.running:
            try:
                state = self.kernel.get_state()

                tasks = self.kernel.task_generator.generate(state)

                for task in tasks:
                    self.kernel.execute_task(task)

                time.sleep(3)

            except Exception as e:
                print("⚠️ Cognition loop error:", e)
