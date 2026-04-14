import json

class UserManager:
    def __init__(self):
        self.users = {}

    def get(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {
                "energy": 4.5,
                "mood": "stable",
                "turns": 0,
                "memory": []
            }
        return self.users[user_id]

    def update(self, user_id, state):
        self.users[user_id] = state

    def all(self):
        return self.users
