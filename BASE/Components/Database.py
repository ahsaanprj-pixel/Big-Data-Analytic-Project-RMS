import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    def read_val(self, query):
        try:
            conn = sqlite3.connect(self.db_file)
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print("Database error:", e)
            return []
