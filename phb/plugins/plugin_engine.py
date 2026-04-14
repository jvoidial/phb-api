import os
import importlib.util

class PluginEngine:
    def __init__(self, path="phb/plugins"):
        self.path = path
        self.plugins = {}

    def load(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        for file in os.listdir(self.path):
            if file.endswith(".py"):
                name = file[:-3]
                full = os.path.join(self.path, file)

                spec = importlib.util.spec_from_file_location(name, full)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)

                self.plugins[name] = mod

    def run(self, msg):
        for name, plugin in self.plugins.items():
            if hasattr(plugin, "run"):
                try:
                    result = plugin.run(msg)
                    if result:
                        return result
                except Exception as e:
                    print(f"⚠️ Plugin error [{name}]:", e)

        return None
