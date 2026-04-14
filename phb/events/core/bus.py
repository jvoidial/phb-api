class EventBus:
    def __init__(self):
        self.subscribers = {}
        self.history = []

    def subscribe(self, event_type, handler):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def publish(self, event_type, payload):
        event = {
            "type": event_type,
            "payload": payload
        }

        self.history.append(event)

        handlers = self.subscribers.get(event_type, [])
        results = []

        for h in handlers:
            try:
                results.append(h(payload))
            except Exception as e:
                results.append(f"error: {e}")

        return results
