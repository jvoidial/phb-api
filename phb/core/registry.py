class ServiceRegistry:
    def __init__(self):
        self.services = {}

    def register(self, name, service):
        print(f"🔌 Registering service: {name}")
        self.services[name] = service

    def get(self, name):
        return self.services.get(name)

    def all(self):
        return list(self.services.keys())
