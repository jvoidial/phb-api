from phb.sandbox.core.plugin_base import PluginBase

class EchoPlugin(PluginBase):
    def run(self, event):
        msg = event.get("msg", "")
        return f"[SANDBOX ECHO] {msg}"
