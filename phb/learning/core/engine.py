from phb.learning.core.experience import ExperienceTracker
from phb.learning.core.behavior import BehaviorModel

class CognitiveLoop:
    def __init__(self):
        self.memory = ExperienceTracker()
        self.behavior = BehaviorModel()

    def step(self, action, success_score=0.5):
        # record experience
        self.memory.record(action, success_score)

        # reinforce behaviour
        self.behavior.update(action, success_score)

    def decide(self):
        return self.behavior.choose()
