class GlobalEventBus:
    def __init__(self):
        self.subscribers = {}
        self.event_queue = []

    def subscribe(self, event_type, handler):
        self.subscribers.setdefault(event_type, []).append(handler)

    def emit(self, event_type, payload):
        self.event_queue.append((event_type, payload))

    def dispatch(self):
        while self.event_queue:
            event_type, payload = self.event_queue.pop(0)

            for handler in self.subscribers.get(event_type, []):
                try:
                    handler(payload)
                except Exception as e:
                    print(f"[EVENT ERROR] {e}")
