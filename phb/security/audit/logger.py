import time

class AuditLogger:
    def log(self, user, action, status):
        entry = {
            "user": user,
            "action": action,
            "status": status,
            "timestamp": time.time()
        }

        print("[AUDIT]", entry)
        return entry
