class PluginBase:
    def run(self, event):
        raise NotImplementedError("Plugin must implement run()")
