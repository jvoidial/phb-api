class Validator:
    def validate(self, upgrade):
        # simple safety rules
        if not upgrade.version:
            return False

        if "rm -rf" in str(upgrade.changes):
            return False

        return True
