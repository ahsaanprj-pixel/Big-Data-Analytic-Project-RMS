from flask import Flask, render_template, redirect, url_for, flash
import logging
from database import Database

# Initialize Flask app with secret key
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Hardcoded secret key (should be stored securely in production)
# Configure logging
logging.basicConfig(filename='rms.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Database
db = Database('restaurant.db')

# Function to initialize database tables
def init_tables():
    fac_conf_query = """
    CREATE TABLE IF NOT EXISTS fac_config(
        id integer PRIMARY KEY, -- Unique identifier for the configuration
        fac_name text NOT NULL, -- Restaurant name
        table_num integer NOT NULL, -- Number of tables in the restaurant
        seat_num integer NOT NULL -- Total number of seats
    );
    """
    menu_conf_query = """
    CREATE TABLE IF NOT EXISTS menu_config(
        id integer PRIMARY KEY, -- Unique identifier for each menu item
        product_name text NOT NULL, -- Name of the menu item
        product_price real NOT NULL -- Price of the menu item
    );
    """
    orders_query = """
    CREATE TABLE IF NOT EXISTS orders(
        id integer PRIMARY KEY, -- Unique order ID
        table_num integer NOT NULL, -- Table number associated with the order
        product_name text NOT NULL, -- Name of the ordered product
        order_quantity integer NOT NULL, -- Quantity ordered
        order_status text NOT NULL -- Status of the order (e.g., Ordered, Cooked)
    );
    """
    cooked_orders = """
    CREATE TABLE IF NOT EXISTS cooked_orders(
        id integer PRIMARY KEY, -- Unique identifier for fulfilled orders
        table_num integer NOT NULL, -- Table number
        product_name text NOT NULL, -- Name of the product
        order_quantity integer NOT NULL, -- Quantity ordered
        order_price integer NOT NULL, -- Total price for the order
        customer_session integer NOT NULL -- Session ID to track customer visits
    );
    """
    db.create_table(fac_conf_query)
    db.create_table(menu_conf_query)
    db.create_table(orders_query)
    db.create_table(cooked_orders)
    db.insert_genconfig()
    logging.info("Database tables initialized")

# Initialize tables on startup
init_tables()

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)