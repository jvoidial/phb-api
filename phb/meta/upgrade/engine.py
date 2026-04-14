from phb.meta.upgrade.validator import Validator
from phb.meta.upgrade.rollback import Rollback

class UpgradeEngine:
    def __init__(self, kernel_path):
        self.kernel_path = kernel_path
        self.validator = Validator()
        self.rollback = Rollback(kernel_path)
        self.applied = set()

    def apply(self, upgrade):
        print(f"⚙️ Applying upgrade: {upgrade.name}")

        if upgrade.version in self.applied:
            print("⚠️ Upgrade already applied")
            return False

        if not self.validator.validate(upgrade):
            print("❌ Upgrade rejected by validator")
            return False

        try:
            # simulate safe patch apply
            for change in upgrade.changes:
                print("✔ Applying change:", change)

            upgrade.applied = True
            self.applied.add(upgrade.version)

            print("🟢 Upgrade applied successfully")

        except Exception as e:
            print("⚠️ Upgrade failed, rolling back:", e)
            self.rollback.restore()

        return True
