class SecurityFirewall:
    def __init__(self):
        self.users = {
            "master.jacobgrainger@gmail.com": "admin",
            "sean2471@gmail.com": "operator"
        }

    def check_permission(self, user, action):
        role = self.users.get(user, "viewer")

        if role == "admin":
            return True

        if role == "operator" and action != "kernel_modify":
            return True

        return False
