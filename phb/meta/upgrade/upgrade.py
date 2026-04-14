class Upgrade:
    def __init__(self, version, name, changes):
        self.version = version
        self.name = name
        self.changes = changes
        self.applied = False
