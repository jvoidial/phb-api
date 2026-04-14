import time
import traceback

class Sandbox:
    def __init__(self, timeout=0.5):
        self.timeout = timeout

    def run(self, plugin, event):
        start = time.time()

        try:
            result = plugin.run(event)

            if time.time() - start > self.timeout:
                return "⛔ Plugin timeout blocked"

            return result

        except Exception as e:
            return f"⚠️ Plugin error isolated: {str(e)}"
