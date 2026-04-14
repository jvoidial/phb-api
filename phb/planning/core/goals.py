class GoalEngine:
    def __init__(self):
        self.goals = []

    def add_goal(self, goal, priority=0.5):
        self.goals.append({
            "goal": goal,
            "priority": priority,
            "progress": 0.0
        })

    def list_goals(self):
        return self.goals
