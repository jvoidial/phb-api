class ServiceManager:
    def __init__(self):
        self.services = {}

    def register(self, name, service):
        self.services[name] = service

    def start_all(self):
        print("⚙️ Starting services:", list(self.services.keys()))

    def get(self, name):
        return self.services.get(name)
