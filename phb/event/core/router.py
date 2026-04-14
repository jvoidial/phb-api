class EventRouter:
    def route(self, event_type, payload):
        priority = payload.get("priority", 0.5)

        if priority > 0.8:
            return "immediate"
        elif priority > 0.4:
            return "normal"
        else:
            return "deferred"
