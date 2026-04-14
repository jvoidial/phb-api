class PriorityEngine:
    def rank(self, goals):
        return sorted(goals, key=lambda g: g["priority"], reverse=True)
