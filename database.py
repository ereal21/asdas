
import sqlite3
from typing import Optional

class Database:
    def __init__(self, path: str = "bot.db"):
        self.path = path
        self._ensure()

    def _ensure(self):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    language TEXT DEFAULT 'en',
                    role TEXT DEFAULT 'USER',
                    balance REAL DEFAULT 0,
                    status TEXT DEFAULT 'None',
                    config_seen INTEGER DEFAULT 0,
                    registered_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cur.execute("PRAGMA table_info(users)")
            cols = [c[1] for c in cur.fetchall()]
            if "role" not in cols:
                cur.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'USER'")
            if "balance" not in cols:
                cur.execute("ALTER TABLE users ADD COLUMN balance REAL DEFAULT 0")
            if "status" not in cols:
                cur.execute(
                    "ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'None'"
                )
            if "config_seen" not in cols:
                cur.execute(
                    "ALTER TABLE users ADD COLUMN config_seen INTEGER DEFAULT 0"
                )
            if "setup_done" not in cols:
                cur.execute(
                    "ALTER TABLE users ADD COLUMN setup_done INTEGER DEFAULT 0"
                )
            if "registered_at" not in cols:
                cur.execute(
                    "ALTER TABLE users ADD COLUMN registered_at TEXT DEFAULT CURRENT_TIMESTAMP"
                )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS admin_status (
                    id INTEGER PRIMARY KEY CHECK (id=1),
                    is_online INTEGER DEFAULT 0
                )
                """
            )
            cur.execute(
                "INSERT OR IGNORE INTO admin_status (id, is_online) VALUES (1, 0)"
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS rdp_configs (
                    user_id INTEGER PRIMARY KEY,
                    email TEXT,
                    password TEXT,
                    ip TEXT,
                    name TEXT,
                    rdp_password TEXT,
                    expiry TEXT
                )
                """
            )
            con.commit()

    def upsert_user(self, user_id: int, username: Optional[str], language: Optional[str] = None):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            # Try insert
            cur.execute(
                "INSERT OR IGNORE INTO users (user_id, username, language) VALUES (?, ?, ?)",
                (user_id, username, language or "en"),
            )
            # Update username and language if provided
            if username is not None:
                cur.execute("UPDATE users SET username=? WHERE user_id=?", (username, user_id))
            if language is not None:
                cur.execute("UPDATE users SET language=? WHERE user_id=?", (language, user_id))
            con.commit()

    def get_language(self, user_id: int) -> str:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            return row[0] if row and row[0] else "en"

    def get_user(self, user_id: int):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT user_id, username, language, role, balance, status, config_seen, registered_at FROM users WHERE user_id=?",
                (user_id,),
            )
            return cur.fetchone()

    def get_user_by_username(self, username: str):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT user_id, username, language, role, balance, status, config_seen, registered_at FROM users WHERE LOWER(username)=LOWER(?)",
                (username,),
            )
            return cur.fetchone()

    def get_balance(self, user_id: int) -> float:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            return row[0] if row else 0

    def get_status(self, user_id: int) -> str:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT status FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            return row[0] if row and row[0] else "None"

    def set_balance(self, user_id: int, amount: float):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET balance=? WHERE user_id=?", (amount, user_id))
            con.commit()

    def set_status(self, user_id: int, status: str):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET status=? WHERE user_id=?", (status, user_id))
            con.commit()

    def get_setup_done(self, user_id: int) -> bool:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT setup_done FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            return bool(row[0]) if row else False

    def set_setup_done(self, user_id: int, done: bool):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET setup_done=? WHERE user_id=?",
                (1 if done else 0, user_id),
            )
            con.commit()

    def get_config_seen(self, user_id: int) -> bool:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT config_seen FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            return bool(row[0]) if row else False

    def set_config_seen(self, user_id: int, seen: bool):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET config_seen=? WHERE user_id=?",
                (1 if seen else 0, user_id),
            )
            con.commit()

    def add_balance(self, user_id: int, amount: float):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id=?",
                (amount, user_id),
            )
            con.commit()

    def deduct_balance(self, user_id: int, amount: float) -> bool:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            if not row or row[0] < amount:
                return False
            new_balance = row[0] - amount
            cur.execute(
                "UPDATE users SET balance=? WHERE user_id=?",
                (new_balance, user_id),
            )
            con.commit()
            return True

    def get_admin_online(self) -> bool:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT is_online FROM admin_status WHERE id=1")
            row = cur.fetchone()
            return bool(row[0]) if row else False

    def set_admin_online(self, online: bool):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE admin_status SET is_online=? WHERE id=1",
                (1 if online else 0,),
            )
            con.commit()

    def set_rdp_config(
        self,
        user_id: int,
        email: str,
        password: str,
        ip: str,
        name: str,
        rdp_password: str,
        expiry: str,
    ):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                """
                REPLACE INTO rdp_configs
                (user_id, email, password, ip, name, rdp_password, expiry)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, email, password, ip, name, rdp_password, expiry),
            )
            con.commit()

    def get_rdp_config(self, user_id: int):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT email, password, ip, name, rdp_password, expiry FROM rdp_configs WHERE user_id=?",
                (user_id,),
            )
            row = cur.fetchone()
            if row:
                return {
                    "email": row[0],
                    "password": row[1],
                    "ip": row[2],
                    "name": row[3],
                    "rdp_password": row[4],
                    "expiry": row[5],
                }
            return None

    def get_setup_users(self):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT user_id, username FROM users WHERE setup_done=1")
            return cur.fetchall()

