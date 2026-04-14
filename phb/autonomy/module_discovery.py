import os
import importlib.util

class ModuleDiscovery:
    def __init__(self, base="phb"):
        self.base = base
        self.modules = {}

    def scan(self):
        print("🔍 Scanning system modules...")

        for root, _, files in os.walk(self.base):
            for f in files:
                if f.endswith(".py") and not f.startswith("__"):
                    full_path = os.path.join(root, f)
                    name = full_path.replace("/", ".").replace(".py", "")

                    self.modules[name] = full_path

        print(f"🧩 Found {len(self.modules)} modules")

    def list(self):
        return list(self.modules.keys())
