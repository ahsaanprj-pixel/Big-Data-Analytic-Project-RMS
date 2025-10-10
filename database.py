import sqlite3
from sqlite3 import Error

# Database class to manage SQLite operations for the restaurant management system
class Database:
    def __init__(self, db):
        # Store the database file path (e.g., 'restaurant.db')
        self.db = db

    def get_connection(self):
        # Return a connection to the SQLite database
        return sqlite3.connect(self.db)

    def create_table(self, create_table_query):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # Execute the provided SQL query to create a table
            cursor.execute(create_table_query)
            conn.commit()
            conn.close()
            # Confirm table creation or existence
            print("✅ Table created or already exists.")
        except Error as e:
            # Handle SQLite errors during table creation
            print("❌ Error creating table:", e)

    def insert_genconfig(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # Create gen_config table to store configuration metadata
            cursor.execute("CREATE TABLE IF NOT EXISTS gen_config (id INTEGER PRIMARY KEY, conf_name text);")
            # Insert default records for facility, menu, and orders configs
            cursor.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)", (1, "fac_config"))
            cursor.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)", (2, "menu_config"))
            cursor.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)", (3, "orders"))
            conn.commit()
            conn.close()
            # Confirm insertion or existence of default configs
            print("✅ Default config records inserted or already exist.")
        except Error as e:
            # Handle SQLite errors during insertion
            print("❌ Error inserting default configs:", e)

    def __del__(self):
        # Indicate Database object cleanup (connections closed in methods)
        print("🔚 Database connection closed.")