import time

class Supervisor:
    def __init__(self):
        self.services = {}

    def register(self, name, process_fn):
        print(f"🧩 Supervisor registering: {name}")
        self.services[name] = {
            "fn": process_fn,
            "alive": True,
            "last_check": time.time()
        }

    def check(self):
        for name, svc in self.services.items():
            try:
                svc["fn"]()
                svc["alive"] = True
            except Exception as e:
                print(f"⚠️ Service failed: {name} → restarting")
                svc["alive"] = False

    def list(self):
        return list(self.services.keys())
