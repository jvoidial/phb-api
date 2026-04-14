from phb.event.core.bus import GlobalEventBus
from phb.event.core.router import EventRouter

class EventEngine:
    def __init__(self):
        self.bus = GlobalEventBus()
        self.router = EventRouter()

    def emit_event(self, event_type, payload):
        mode = self.router.route(event_type, payload)

        self.bus.emit(event_type, {
            "mode": mode,
            **payload
        })

    def tick(self):
        self.bus.dispatch()
