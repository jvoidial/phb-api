class PolicyEngine:
    def evaluate(self, action, risk=0.0):
        if risk > 0.8:
            return "deny"

        if risk > 0.5:
            return "require_approval"

        return "allow"
