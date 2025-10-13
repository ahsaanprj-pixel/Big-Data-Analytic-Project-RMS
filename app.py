from flask import Flask, render_template
import sqlite3

# Initialize Flask application
app = Flask(__name__)
# Set secret key for session management and security
app.secret_key = 'your_secret_key'

# Import database module and create database instance
from database import Database
db = Database('restaurant.db')

def init_tables():
    fac_conf_query = """
    CREATE TABLE IF NOT EXISTS fac_config(
        id integer PRIMARY KEY,
        fac_name text NOT NULL,
        table_num integer NOT NULL,
        seat_num integer NOT NULL
    );
    """
    
    menu_conf_query = """
    CREATE TABLE IF NOT EXISTS menu_config(
        id integer PRIMARY KEY,
        product_name text NOT NULL,
        product_price real NOT NULL
    );
    """
   
    orders_query = """
    CREATE TABLE IF NOT EXISTS orders(
        id integer PRIMARY KEY,
        table_num integer NOT NULL,
        product_name text NOT NULL,
        order_quantity integer NOT NULL,
        order_status text NOT NULL
    );
    """
   
    cooked_orders = """
    CREATE TABLE IF NOT EXISTS cooked_orders(
        id integer PRIMARY KEY,
        table_num integer NOT NULL,
        product_name text NOT NULL,
        order_quantity integer NOT NULL,
        order_price integer NOT NULL,
        customer_session integer NOT NULL
    );
    """
    # Execute table creation queries
    db.create_table(fac_conf_query)
    db.create_table(menu_conf_query)
    db.create_table(orders_query)
    db.create_table(cooked_orders)
    # Insert default configuration records
    db.insert_genconfig()

# Initialize database tables when module is imported
init_tables()

# Route for the main index page
@app.route('/')
def index():
    # Retrieve facility name from database
    fac_info = db.read_val("SELECT fac_name FROM fac_config LIMIT 1")
    # Use restaurant name from database or default name if not found
    restaurant_name = fac_info[0][0] if fac_info else "Restaurant Management System"
    # Render the main index template with restaurant name
    return render_template('index.html', restaurant_name=restaurant_name)

# Route for configuration page
@app.route('/config')
def config():
    return "Configuration page - enhanced in Wk 3"

# Route for creating new orders
@app.route('/create_order')
def create_order():
    return "Create Order page - enhanced in Wk 4"

# Route for kitchen display
@app.route('/kitchen')
def kitchen():
    return "Kitchen page - enhanced in Wk 5"

# Route for printing receipts
@app.route('/print_receipt')
def print_receipt():
    return "Print Receipt page - enhanced in Wk 6"

# Main entry point for running the Flask application
if __name__ == '__main__':
    app.run(debug=True)
    
    