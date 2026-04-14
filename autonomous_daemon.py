import time
from user_manager import UserManager

users = UserManager()

def decay_loop():
    while True:
        for uid, state in users.all().items():
            state["energy"] = max(1.0, state["energy"] - 0.01)

        time.sleep(60)
