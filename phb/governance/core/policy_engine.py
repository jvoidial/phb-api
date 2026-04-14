class PolicyEngine:
    def __init__(self):
        self.rules = {
            "echo": True,
            "analyzer": True,
        }

    def allowed(self, agent_name, action="run"):
        return self.rules.get(agent_name, False)

    def set_rule(self, agent_name, value):
        self.rules[agent_name] = value
