# import sqlite3

# class Database:
#     def __init__(self, db_file):
#         self.db_file = db_file

#     def read_val(self, query):
#         try:
#             conn = sqlite3.connect(self.db_file)
#             cur = conn.cursor()
#             cur.execute(query)
#             rows = cur.fetchall()
#             conn.close()
#             return rows
#         except sqlite3.Error as e:
#             print("Database error:", e)
#             return []







# ===============================================================
# Week 2 - Database Setup and Understanding
# ---------------------------------------------------------------
# This file handles all SQLite database operations for the
# Restaurant Management System.
# The database stores configurations, menu items, and orders.
# ===============================================================

import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self, db):
        """
        Initialize the database connection.
        ------------------------------------
        - Connects to the SQLite database file (db)
        - Creates a cursor object for running SQL commands
        - Ensures that a basic configuration table exists
        - Calls insert_genconfig() to insert default records
        """
        self.conn = sqlite3.connect(db)   # ✅ connect to DB file
        self.cur = self.conn.cursor()     # ✅ create a cursor for SQL commands

        # ✅ Create main configuration table if not already present
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS gen_config (id INTEGER PRIMARY KEY, conf_name text);"
        )
        self.conn.commit()

        # ✅ Insert initial configuration values (fac_config, menu_config, orders)
        self.insert_genconfig()

    # ===============================================================
    # Function: create_table
    # Used for creating any new table dynamically from other modules
    # Example: creating a menu table or orders table in later weeks
    # ===============================================================
    def create_table(self, create_table_query):
        try:
            cursor = self.cur
            cursor.execute(create_table_query)
            self.conn.commit()
        except Error as e:
            print("❌ Error creating table:", e)

    # ===============================================================
    # Function: insert_genconfig
    # Inserts basic default configuration data into gen_config table
    # ===============================================================
    def insert_genconfig(self):
        try:
            self.cur.execute(
                "INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)",
                (1, "fac_config")
            )
            self.cur.execute(
                "INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)",
                (2, "menu_config")
            )
            self.cur.execute(
                "INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)",
                (3, "orders")
            )
            self.conn.commit()
            print("✅ Default config records inserted or already exist.")
        except Error as e:
            print("❌ Error inserting default configs:", e)

    # ===============================================================
    # Function: insert_spec_config
    # Used to insert new records (menu, order, etc.)
    # ===============================================================
    def insert_spec_config(self, insert_query, values):
        try:
            con = self.cur
            con.execute(insert_query, values)
            self.conn.commit()
        except Error as e:
            print("❌ Insert error:", e)

    # ===============================================================
    # Function: update
    # Used to modify existing records
    # ===============================================================
    def update(self, update_query, values):
        try:
            con = self.cur
            con.execute(update_query, values)
            self.conn.commit()
        except Error as e:
            print("❌ Update error:", e)

    # ===============================================================
    # Function: read_val
    # Used to fetch records from database tables
    # ===============================================================
    def read_val(self, read_query, table_num=''):
        try:
            con = self.cur
            # If WHERE clause is used, run query with parameter
            if "WHERE" in read_query:
                con.execute(read_query, table_num)
                rows = con.fetchall()
            else:
                con.execute(read_query)
                rows = con.fetchall()
            return rows
        except Error as e:
            print("❌ Read error:", e)

    # ===============================================================
    # Function: delete_val
    # Used to remove specific records from tables
    # ===============================================================
    def delete_val(self, delete_query, item_id):
        try:
            con = self.cur
            con.execute(delete_query, item_id)
            self.conn.commit()
        except Error as e:
            print("❌ Delete error:", e)

    # ===============================================================
    # Destructor: closes database connection when object is deleted
    # ===============================================================
    def __del__(self):
        self.conn.close()
