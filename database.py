import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db):
        # Initialize database with the provided database file path
        self.db = db

    def get_connection(self):
        # Create and return a new database connection
        return sqlite3.connect(self.db)

    def create_table(self, create_table_query):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            conn.commit()
            conn.close()
            print("✅ Table created or already exists.")
        except Error as e:
            print("❌ Error creating table:", e)

    def insert_genconfig(self):
        # Create gen_config table and insert default configuration records
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # Create table if it doesn't exist
            cursor.execute("CREATE TABLE IF NOT EXISTS gen_config (id INTEGER PRIMARY KEY, conf_name text);")
            # Insert default configuration types with unique IDs
            cursor.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)", (1, "fac_config"))
            cursor.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)", (2, "menu_config"))
            cursor.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)", (3, "orders"))
            conn.commit()
            conn.close()
            print("✅ Default config records inserted or already exist.")
        except Error as e:
            print("❌ Error inserting default configs:", e)

    def insert_spec_config(self, insert_query, values):
        # Insert specific configuration data using provided query and parameters
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(insert_query, values)
            conn.commit()
            conn.close()
            print("✅ Insert successful.")
        except Error as e:
            print("❌ Insert error:", e)

    def update(self, update_query, values):
        # Update existing records in the database
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(update_query, values)
            conn.commit()
            conn.close()
            print("✅ Update successful.")
        except Error as e:
            print("❌ Update error:", e)

    def read_val(self, read_query, params=()):
        # Read data from database using SELECT query with optional parameters
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(read_query, params)
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Error as e:
            print("❌ Read error:", e)
            return []

    def delete_val(self, delete_query, params):
        # Delete records from database using provided query and parameters
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(delete_query, params)
            conn.commit()
            conn.close()
            print("✅ Delete successful.")
        except Error as e:
            print("❌ Delete error:", e)

    def __del__(self):
        # Destructor method that runs when object is destroyed
        print("🔚 Database connection closed.")