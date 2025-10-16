
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import html

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    db.create_table(fac_conf_query)
    db.create_table(menu_conf_query)
    db.create_table(orders_query)
    db.create_table(cooked_orders)
    db.insert_genconfig()

init_tables()

@app.route('/')
def index():
    fac_info = db.read_val("SELECT fac_name FROM fac_config LIMIT 1")
    restaurant_name = fac_info[0][0] if fac_info else "Restaurant Management System"
    return render_template('index.html', restaurant_name=restaurant_name)

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        fac_name = html.escape(request.form.get('fac_name', '').strip())
        table_num = request.form.get('table_num')
        seat_num = request.form.get('seat_num')
        if fac_name and table_num and seat_num:
            try:
                table_num = int(table_num)
                seat_num = int(seat_num)
                if table_num > 50:
                    flash('Maximum number of tables cannot exceed 50!')
                elif seat_num > (table_num * 8):
                    flash(f'Maximum number of seats cannot exceed {table_num * 8}!')
                else:
                    existing = db.read_val("SELECT * FROM fac_config")
                    if existing:
                        db.update("UPDATE fac_config SET fac_name=?, table_num=?, seat_num=? WHERE id=1", (fac_name, table_num, seat_num))
                    else:
                        db.insert_spec_config("INSERT INTO fac_config VALUES (?, ?, ?, ?)", (1, fac_name, table_num, seat_num))
                    flash('Facility config saved!')
            except ValueError:
                flash('Table and seat numbers must be valid integers!')

        product_name = html.escape(request.form.get('product_name', '').strip())
        product_price = request.form.get('product_price')
        if product_name and product_price:
            try:
                product_price = float(product_price)
                if len(product_name) > 20:
                    flash('Product name must be 20 characters or less!')
                elif product_price > 10000000:
                    flash('Product price exceeds maximum allowed (10 million)!')
                else:
                    if db.read_val("SELECT id FROM menu_config WHERE product_name=?", (product_name,)):
                        flash('Product name already exists!')
                    else:
                        last_id = db.read_val("SELECT id FROM menu_config ORDER BY id DESC LIMIT 1")
                        pr_id = last_id[0][0] + 1 if last_id else 1
                        db.insert_spec_config("INSERT INTO menu_config VALUES (?, ?, ?)", (pr_id, product_name, product_price))
                        flash('Product added!')
            except ValueError:
                flash('Product price must be a valid number!')

        remove_id = request.form.get('remove_id')
        if remove_id:
            db.delete_val("DELETE FROM menu_config WHERE id=?", (remove_id,))
            flash('Product removed!')

        return redirect(url_for('config'))

    fac_config = db.read_val("SELECT * FROM fac_config LIMIT 1")
    menu_items = db.read_val("SELECT * FROM menu_config")
    return render_template('config.html', fac_config=fac_config[0] if fac_config else None, menu_items=menu_items)

@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    menu_items = db.read_val("SELECT product_name FROM menu_config")
    fac_info = db.read_val("SELECT table_num FROM fac_config LIMIT 1")
    max_tables = fac_info[0][0] if fac_info else 50
    if not menu_items:
        flash('Please configure menu items first in the Config page!')
    if request.method == 'POST':
        table_num = request.form.get('table_num')
        products = request.form.getlist('product_name')
        quantities = request.form.getlist('quantity')
        if table_num and products and quantities:
            try:
                table_num = int(table_num)
                if table_num < 1 or table_num > max_tables:
                    flash(f'Table number must be between 1 and {max_tables}!')
                    return redirect(url_for('create_order'))
                valid = True
                for i, product in enumerate(products):
                    if product == '' or product == 'Select a meal':
                        flash('Please select a valid meal for all rows!')
                        valid = False
                        break
                    try:
                        quantities[i] = int(quantities[i])
                        if quantities[i] < 1 or quantities[i] > 100:
                            flash('Quantity must be between 1 and 100!')
                            valid = False
                            break
                    except ValueError:
                        flash('Quantity must be a valid number!')
                        valid = False
                        break
                if valid:
                    for i, product in enumerate(products):
                        if product != '' and product != 'Select a meal':
                            quantity = quantities[i]
                            last_id = db.read_val("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
                            order_id = last_id[0][0] + 1 if last_id else 1
                            db.insert_spec_config("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", (order_id, table_num, product, quantity, 'Ordered'))
                    flash('Order sent to kitchen!')
                    return redirect(url_for('create_order'))
            except ValueError:
                flash('Table number must be a valid number!')
        else:
            flash('Please fill all fields, including at least one product!')
        return redirect(url_for('create_order'))
    return render_template('create_order.html', menu_items=menu_items, max_tables=max_tables)

@app.route('/kitchen')
def kitchen():
    return "Kitchen page - enhanced in Week 5"

@app.route('/print_receipt')
def print_receipt():
    return "Print Receipt page - enhanced in Week 6"

if __name__ == '__main__':
    app.run(debug=True)
