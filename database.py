# Week 1: Basic database connection setup
import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db):
        self.db = db

    def get_connection(self):
        # Basic connection method
        return sqlite3.connect(self.db)

    def create_table(self, create_table_query):
        # Basic table creation method
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            conn.commit()
            conn.close()
            print("✅ Table created or already exists.")
        except Error as e:
            print("❌ Error creating table:", e)

    # Other methods will be added in Week 2