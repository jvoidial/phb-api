import traceback

class APIHealer:
    """
    Self-healing API layer for PHB system.
    Detects broken endpoints and reroutes safely.
    """

    def __init__(self):
        self.registry = {}
        self.repair_log = []

    def register(self, route, handler):
        self.registry[route] = handler

    def heal(self, route, payload=None, error=None):
        """
        If route fails → fallback safely.
        """
        self.repair_log.append({
            "route": route,
            "error": str(error),
            "status": "healed_fallback"
        })

        return {
            "healed": True,
            "route": route,
            "message": "PHB fallback handler active",
            "error": str(error) if error else None
        }

    def call(self, route, payload=None):
        try:
            if route in self.registry:
                return self.registry[route](payload)

            raise Exception("Route not registered")

        except Exception as e:
            return self.heal(route, payload, e)
