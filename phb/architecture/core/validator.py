class UpgradeValidator:
    def validate(self, patch_name):
        # SAFE RULES (simple but strict)
        blocked = ["kernel.exec", "rm -rf", "os.system", "fork bomb"]

        for b in blocked:
            if b in patch_name:
                return False

        return True
