import os
import importlib.util

class PluginManager:
    def __init__(self):
        self.plugins = {}

    def load(self):
        path = "phb/plugins"
        os.makedirs(path, exist_ok=True)

        for f in os.listdir(path):
            if f.endswith(".py"):
                name = f[:-3]
                full = os.path.join(path, f)

                spec = importlib.util.spec_from_file_location(name, full)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)

                self.plugins[name] = mod

    def run(self, msg):
        for p in self.plugins.values():
            if hasattr(p, "run"):
                out = p.run(msg)
                if out:
                    return out
        return None
