class StageValidator:
    def validate(self, design):
        return {
            "design": design,
            "stable": design.get("score", 0) > 0.7,
            "risk": design.get("risk", 1.0)
        }
