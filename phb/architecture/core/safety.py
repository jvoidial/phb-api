class SafetyController:
    def validate(self, before, after):
        for node in before["nodes"]:
            if after["nodes"][node]["load"] > 1.2:
                return False
        return True
