from phb.planning.core.goals import GoalEngine
from phb.planning.core.decomposer import TaskDecomposer
from phb.planning.core.priority import PriorityEngine

class PlanningEngine:
    def __init__(self):
        self.goals = GoalEngine()
        self.decomposer = TaskDecomposer()
        self.priority = PriorityEngine()

    def add_goal(self, goal, priority=0.5):
        self.goals.add_goal(goal, priority)

    def plan(self):
        ranked = self.priority.rank(self.goals.list_goals())

        plans = {}

        for g in ranked:
            plans[g["goal"]] = self.decomposer.breakdown(g["goal"])

        return plans
