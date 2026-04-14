class PatchValidator:
    def validate(self, patch):
        if patch["risk_level"] > 0.7:
            return {"approved": False, "reason": "risk too high"}

        if len(patch["changes"]) == 0:
            return {"approved": False, "reason": "empty patch"}

        return {"approved": True}
