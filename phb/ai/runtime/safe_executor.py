class SafeExecutor:
    def run(self, plugin, event):
        try:
            if hasattr(plugin, "run"):
                return plugin.run(event)
        except Exception as e:
            return f"⚠️ Plugin blocked: {e}"
