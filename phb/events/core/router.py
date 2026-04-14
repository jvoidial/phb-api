from phb.events.core.adaptive import AdaptiveSignalLayer

class AdaptiveRouter:
    def __init__(self, bus):
        self.bus = bus
        self.adaptive = AdaptiveSignalLayer()

    def route(self, event_type, payload):
        self.adaptive.reinforce(event_type)
        return self.bus.publish(event_type, payload)

    def tick(self):
        self.adaptive.decay()
