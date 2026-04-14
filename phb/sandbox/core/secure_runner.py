from phb.sandbox.core.sandbox import Sandbox

class SecureRunner:
    def __init__(self):
        self.sandbox = Sandbox()
        self.plugins = []

    def register(self, plugin):
        self.plugins.append(plugin)

    def execute(self, event):
        results = []

        for p in self.plugins:
            try:
                results.append(self.sandbox.run(p, event))
            except Exception as e:
                results.append(f"⚠️ sandbox crash prevented: {e}")

        return results
