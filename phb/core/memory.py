import os
import sqlite3
import threading

DB = "phb/state/memory.db"
lock = threading.Lock()

class Memory:
    def __init__(self):
        os.makedirs("phb/state", exist_ok=True)
        self.conn = sqlite3.connect(DB, check_same_thread=False)
        self._init()

    def _init(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            user TEXT,
            msg TEXT
        )
        """)

    def save(self, user, msg):
        with lock:
            self.conn.execute("INSERT INTO memory VALUES (?,?)", (user, msg))
            self.conn.commit()

    def get_count(self, user):
        cur = self.conn.execute(
            "SELECT COUNT(*) FROM memory WHERE user=?",
            (user,)
        )
        return cur.fetchone()[0]
