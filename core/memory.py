import os
import sqlite3

DB = "state/memory.db"

class Memory:
    def __init__(self):
        os.makedirs("state", exist_ok=True)
        self.conn = sqlite3.connect(DB, check_same_thread=False)
        self._init()

    def _init(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            user TEXT,
            message TEXT,
            tag TEXT DEFAULT 'general'
        )
        """)
        self.conn.commit()

    def save(self, user, msg, tag="general"):
        c = self.conn.cursor()
        c.execute("INSERT INTO memory VALUES (?,?,?)", (user, msg, tag))
        self.conn.commit()

    def fetch(self, user):
        c = self.conn.cursor()
        c.execute("SELECT message FROM memory WHERE user=?", (user,))
        return [r[0] for r in c.fetchall()]
