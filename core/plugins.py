import os
import importlib.util

PLUGIN_DIR = "plugins"

class PluginManager:
    def __init__(self):
        self.plugins = {}

    def load_plugins(self):
        if not os.path.exists(PLUGIN_DIR):
            os.makedirs(PLUGIN_DIR)

        for file in os.listdir(PLUGIN_DIR):
            if file.endswith(".py"):
                name = file[:-3]
                path = os.path.join(PLUGIN_DIR, file)

                spec = importlib.util.spec_from_file_location(name, path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)

                self.plugins[name] = mod

    def run(self, msg):
        for name, plugin in self.plugins.items():
            if hasattr(plugin, "run"):
                result = plugin.run(msg)
                if result:
                    return result
        return None
