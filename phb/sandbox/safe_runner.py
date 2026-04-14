import traceback

class Sandbox:
    def run(self, plugin, data):
        try:
            if hasattr(plugin, "run"):
                return plugin.run(data)
        except Exception as e:
            print("🛡️ Sandbox blocked crash:")
            print(traceback.format_exc())
            return None
