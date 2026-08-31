import sqlite3
from datetime import timedelta


class DataBasePredictedMessages:
    def __init__(self, path: str = 'predicted_messages.bd'):
        self.db = sqlite3.connect(path, timeout=10, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.db.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""
               CREATE TABLE IF NOT EXISTS friend (
                    message_id TEXT PRIMARY KEY,
                    date DATETIME,
                    predicted_message TEXT,
                    used SMALLINT
               )""")
        self.db.commit()

    def add_message(self, predicted_text: str, date: str, message_id: str) -> None:
        self.c.execute("""
            INSERT INTO friend (date, predicted_message, message_id, used) VALUES (?, ?, ?, 0)
        """, (date, predicted_text, message_id))
        self.db.commit()

    def set_used(self, message_id: str):
        self.c.execute("""
            UPDATE friend
            SET used = used + 1
            WHERE message_id = ?
        """, (message_id,))
        self.db.commit()

    def close(self):
        self.db.close()

class DataBaseChat:
    def __init__(self, path: str = 'chat.bd'):
            self.db = sqlite3.connect(path, timeout=10, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.c = self.db.cursor()
            self.create_table()

    def create_table(self) -> None:
        self.c.execute("""
               CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATETIME,
                    person TEXT,
                    message TEXT
               )""")
        self.db.commit()

    def add_message(self, message: str, date, person: str) -> None:
        date = date - timedelta(hours=4)

        self.c.execute("""
            INSERT INTO history (date, person, message) VALUES (?, ?, ?)
        """, (date, person, message))
        self.db.commit()

    def get_chat_history(self, date):
        date = date - timedelta(hours=4)

        self.c.execute("""
            SELECT person, message
            FROM history
            WHERE strftime('%Y-%m-%d', date) = strftime('%Y-%m-%d', ?)
            ORDER BY date ASC
        """, (date,))

        data = self.c.fetchall()

        return data
                
    def close(self):
            self.db.close()


chat_bd = DataBaseChat()
predicted_messages_bd = DataBasePredictedMessages()
