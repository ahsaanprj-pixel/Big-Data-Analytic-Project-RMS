
from flask import Flask, render_template, request, redirect, url_for, flash
from bs4 import BeautifulSoup
import os
import webbrowser
import sqlite3
import html

app = Flask(__name__)
app.secret_key = 'your_secret_key'

from database import Database
db = Database('restaurant.db')

def migrate_database():
    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(cooked_orders)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'customer_session' not in columns:
            cursor.execute("ALTER TABLE cooked_orders ADD COLUMN customer_session INTEGER NOT NULL DEFAULT 1")
            conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"❌ Database migration error: {str(e)}")
        flash('Failed to update database schema. Please manually add customer_session column to cooked_orders.')

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
    migrate_database()

init_tables()

@app.route('/')
def index():
    fac_info = db.read_val("SELECT fac_name FROM fac_config LIMIT 1")
    restaurant_name = fac_info[0][0] if fac_info else "Restaurant Management System"
    return render_template('index.html', restaurant_name=restaurant_name)

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        # -------------------- FACILITY CONFIG --------------------
        fac_name = html.escape(request.form.get('fac_name', '').strip())
        table_num = request.form.get('table_num')
        seat_num  = request.form.get('seat_num')

        if fac_name and table_num and seat_num:
            try:
                table_num = int(table_num)
                seat_num  = int(seat_num)

                if table_num > 50:
                    flash('Maximum number of tables cannot exceed 50!')
                elif seat_num > table_num * 8:
                    flash(f'Maximum number of seats cannot exceed {table_num * 8}!')
                else:
                    exists = db.read_val("SELECT id FROM fac_config LIMIT 1")
                    query  = "UPDATE fac_config SET fac_name=?, table_num=?, seat_num=? WHERE id=1" \
                             if exists else \
                             "INSERT INTO fac_config VALUES (1, ?, ?, ?)"
                    db.update(query, (fac_name, table_num, seat_num))
                    flash('Facility config saved!')
            except ValueError:
                flash('Table and seat numbers must be valid integers!')

        # -------------------- ADD MENU ITEM --------------------
        product_name  = html.escape(request.form.get('product_name', '').strip())
        product_price = request.form.get('product_price')

        if product_name and product_price:
            try:
                product_price = float(product_price)

                if len(product_name) > 20:
                    flash('Product name must be 20 characters or less!')
                elif product_price > 10_000_000:
                    flash('Product price exceeds maximum allowed (10 million)!')
                elif db.read_val("SELECT id FROM menu_config WHERE product_name=?", (product_name,)):
                    flash('Product name already exists!')
                else:
                    last = db.read_val("SELECT MAX(id) FROM menu_config")
                    new_id = (last[0][0] or 0) + 1
                    db.insert_spec_config(
                        "INSERT INTO menu_config VALUES (?, ?, ?)",
                        (new_id, product_name, product_price)
                    )
                    flash('Product added!')
            except ValueError:
                flash('Product price must be a valid number!')

        # -------------------- REMOVE MENU ITEM --------------------
        remove_id = request.form.get('remove_id')
        if remove_id:
            db.delete_val("DELETE FROM menu_config WHERE id=?", (remove_id,))
            flash('Product removed!')

        return redirect(url_for('config'))

    # -------------------- LOAD PAGE DATA --------------------
    fac_config = db.read_val("SELECT * FROM fac_config LIMIT 1")
    menu_items = db.read_val("SELECT * FROM menu_config")

    return render_template(
        'config.html',
        fac_config=fac_config[0] if fac_config else None,
        menu_items=menu_items
    )


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

        if not table_num or not products or not quantities:
            flash('Please fill all fields, including at least one product!')
            return redirect(url_for('create_order'))

        try:
            table_num = int(table_num)
            if table_num < 1 or table_num > max_tables:
                flash(f'Table number must be between 1 and {max_tables}!')
                return redirect(url_for('create_order'))

            # Validate products & quantities
            # products = ['Pizza', 'Burger', 'Pasta']
            # enumerate(products) → returns both the index and the value for each element in the list.
            # list(enumerate(products))
# Output: [(0, 'Pizza'), (1, 'Burger'), (2, 'Pasta')]
            for i, product in enumerate(products):
                if product in ('', 'Select a meal'):
                    flash('Please select a valid meal for all rows!')
                    return redirect(url_for('create_order'))
                try:
                    qty = int(quantities[i])
                    if qty < 1 or qty > 100:
                        flash('Quantity must be between 1 and 100!')
                        return redirect(url_for('create_order'))
                except ValueError:
                    flash('Quantity must be a valid number!')
                    return redirect(url_for('create_order'))

            # Insert orders
            last_id = db.read_val("SELECT MAX(id) FROM orders")
            next_id = (last_id[0][0] if last_id and last_id[0][0] else 0) + 1

            for i, product in enumerate(products):
                db.insert_spec_config(
                    "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
                    (next_id + i, table_num, product, int(quantities[i]), 'Ordered')
                )

            flash('Order sent to kitchen!')
            return redirect(url_for('create_order'))

        except ValueError:
            flash('Table number must be a valid number!')
            return redirect(url_for('create_order'))

    return render_template('create_order.html', menu_items=menu_items, max_tables=max_tables)

@app.route('/kitchen', methods=['GET', 'POST'])
def kitchen():
    if request.method == 'POST':
        action = request.form.get('action')
        table_num = request.form.get('table_num')

        if action == 'mark_cooked' and table_num:
            product_name = request.form.get('product_name')
            if product_name:
                db.update("UPDATE orders SET order_status='Cooked' WHERE table_num=? AND product_name=?", 
                          (table_num, product_name))
                flash('Item marked as cooked!')

        elif action == 'fulfill_order' and table_num:
            try:
                table_num = int(table_num)
                cooked = db.read_val("SELECT * FROM orders WHERE table_num=? AND order_status='Cooked'", (table_num,))
                if not cooked:
                    flash('No cooked items to fulfill for this table!')
                else:
                    last_session = db.read_val("SELECT MAX(customer_session) FROM cooked_orders WHERE table_num=?", (table_num,))
                    customer_session = (last_session[0][0] + 1) if last_session and last_session[0][0] else 1

                    last_id = db.read_val("SELECT id FROM cooked_orders ORDER BY id DESC LIMIT 1")
                    next_id = last_id[0][0] + 1 if last_id else 1

                    for i, order in enumerate(cooked):
                        price_res = db.read_val("SELECT product_price FROM menu_config WHERE product_name=?", (order[2],))
                        price = price_res[0][0] if price_res else 0
                        #order qty
                        total_price = order[3] * price
                        try:
                            db.insert_spec_config("INSERT INTO cooked_orders VALUES (?, ?, ?, ?, ?, ?)", 
                                                 (next_id + i, order[1], order[2], order[3], total_price, customer_session))
                        except sqlite3.OperationalError as e:
                            if "no such column: customer_session" in str(e):
                                db.insert_spec_config("INSERT INTO cooked_orders (id, table_num, product_name, order_quantity, order_price) VALUES (?, ?, ?, ?, ?)",
                                                     (next_id + i, order[1], order[2], order[3], total_price))
                            else:
                                raise e
                    db.delete_val("DELETE FROM orders WHERE table_num=? AND order_status='Cooked'", (table_num,))
                    flash('Order fulfilled and moved to cooked orders!')
            except ValueError:
                flash('Invalid table number!')
        return redirect(url_for('kitchen'))

   # Get all unique table numbers from orders
    tables = db.read_val("SELECT DISTINCT table_num FROM orders ORDER BY table_num")

    # Get orders grouped by product and status for each table
    orders_by_table = {}
    for t in tables:
        table_num = t[0]
        orders_by_table[table_num] = db.read_val("""
            SELECT MIN(id) as id, product_name, SUM(order_quantity) as qty, order_status
            FROM orders WHERE table_num=? GROUP BY product_name, order_status
        """, (table_num,))

    # Check if any order is still 'Ordered' for each table
    has_ordered = {table_num: any(o[3] == 'Ordered' for o in orders_by_table[table_num]) for table_num in orders_by_table}


    return render_template('kitchen.html', orders_by_table=orders_by_table, has_ordered=has_ordered)

@app.route('/print_receipt', methods=['GET', 'POST'])
def print_receipt():
    fac_info = db.read_val("SELECT fac_name, table_num FROM fac_config LIMIT 1")
    restaurant_name = fac_info[0][0] if fac_info else "Restaurant"
    max_tables = fac_info[0][1] if fac_info else 50
    orders = []
    if request.method == 'POST':
        table_num = request.form.get('table_num')
        action = request.form.get('action')
        if action == 'new_customer' and table_num:
            try:
                table_num = int(table_num)
                if table_num < 1 or table_num > max_tables:
                    flash(f'Table number must be between 1 and {max_tables}!')
                else:
                    db.delete_val("DELETE FROM cooked_orders WHERE table_num=?", (table_num,))
                    flash(f'New customer session started for Table {table_num}!')
                return redirect(url_for('print_receipt'))
            except ValueError:
                flash('Table number must be a valid integer!')
        if table_num:
            try:
                table_num = int(table_num)
                if table_num < 1 or table_num > max_tables:
                    flash(f'Table number must be between 1 and {max_tables}!')
                else:
                    conn = sqlite3.connect('restaurant.db')
                    cursor = conn.cursor()
                    cursor.execute("PRAGMA table_info(cooked_orders)")
                    columns = [col[1] for col in cursor.fetchall()]
                    conn.close()
                    if 'customer_session' in columns:
                        last_session = db.read_val("SELECT MAX(customer_session) FROM cooked_orders WHERE table_num=?", (table_num,))
                        customer_session = last_session[0][0] if last_session and last_session[0][0] is not None else None
                        if customer_session is not None:
                            orders = db.read_val("""
                                SELECT MIN(id) as id, product_name, SUM(order_quantity) as qty, SUM(order_price) as price
                                FROM cooked_orders WHERE table_num=? AND customer_session=?
                                GROUP BY product_name
                            """, (table_num, customer_session))
                        else:
                            orders = []
                    else:
                        orders = db.read_val("""
                            SELECT MIN(id) as id, product_name, SUM(order_quantity) as qty, SUM(order_price) as price
                            FROM cooked_orders WHERE table_num=?
                            GROUP BY product_name
                        """, (table_num,))
                        customer_session = 1
                    if orders:
                        template_path = os.path.join(app.root_path, 'templates', 'order_template.html')
                        try:
                            with open(template_path, encoding='utf-8') as f:
                                soup = BeautifulSoup(f, 'html.parser')
                        except FileNotFoundError:
                            soup = BeautifulSoup("""
                            <!DOCTYPE html>
                            <html>
                            <head>
                                <style>
                                    .container { width: 595pt; height: 842pt; display: flex; flex-direction: column; align-items: center; }
                                    .text { top: 30pt; position: absolute; }
                                    .text1 { top: 80pt; position: absolute; font-size: 24pt; }
                                    .text2 { top: 130pt; left: 85pt; position: absolute; font-size: 20pt; }
                                    .text3 { top: 130pt; left: 275pt; position: absolute; font-size: 20pt; }
                                    .text4 { top: 130pt; right: 85pt; position: absolute; font-size: 20pt; }
                                    hr { border: none; border-top: 1px dotted #000; height: 1px; width: 80%; top: 150pt; position: absolute; }
                                    @media print { @page { size: A4; } }
                                </style>
                            </head>
                            <body onload="window.print()">
                                <div class='container'>
                                    <h1 class='text'>Fac_name</h1>
                                    <span class='text1'>t_num</span>
                                    <span class='text2'>Name</span>
                                    <span class='text3'>Quantity</span>
                                    <span class='text4'>Price</span>
                                    <hr>
                                </div>
                            </body>
                            </html>
                            """, 'html.parser')
                            flash('Warning: Receipt template not found, using fallback template.')
                        soup.find(text="Fac_name").replace_with(restaurant_name)
                        soup.find(text="t_num").replace_with(f"Table № {table_num}")
                        top_pad = 0
                        total_qty = 0
                        total_price = 0.0
                        for order in orders:
                            name = order[1]
                            qty = order[2]
                            price = order[3]
                            total_qty += qty
                            total_price += price
                            p_name = f"<span style='top:{150 + (top_pad * 20)}pt; left:85pt; position:absolute; font-size:20pt;'>{name}</span>"
                            p_qty = f"<span style='top:{150 + (top_pad * 20)}pt; left:275pt; position:absolute; font-size:20pt;'>x{qty}</span>"
                            p_price = f"<span style='top:{150 + (top_pad * 20)}pt; right:85pt; position:absolute; font-size:20pt;'>{price:.2f}</span>"
                            soup.div.append(BeautifulSoup(p_name, "html.parser"))
                            soup.div.append(BeautifulSoup(p_qty, "html.parser"))
                            soup.div.append(BeautifulSoup(p_price, "html.parser"))
                            top_pad += 1
                        hr_style = f"top:{170 + (top_pad * 20)}pt;"
                        hr = f"<hr style='{hr_style}' />"
                        total_pos = 170 + (top_pad * 20) + 20
                        total = f"<span style='top:{total_pos}pt; left:85pt; position:absolute; font-size:20pt;'>Total ordered products: {total_qty}, total price: {total_price:.2f} ft</span>"
                        soup.div.append(BeautifulSoup(hr, "html.parser"))
                        soup.div.append(BeautifulSoup(total, "html.parser"))
                        receipt_file = f"receipt_{table_num}_session_{customer_session or 'legacy'}.html"
                        with open(receipt_file, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                        webbrowser.open('file://' + os.path.realpath(receipt_file))
                        flash('Receipt generated and opened for printing!')
                    else:
                        flash(f'No cooked orders found for table {table_num} in the current session!')
            except ValueError:
                flash('Table number must be a valid integer!')
            except sqlite3.OperationalError as e:
                flash('Database error while generating receipt. Please ensure database is updated.')
            except Exception as e:
                flash('Error generating receipt. Please try again.')
        else:
            flash('Please enter a table number!')
    return render_template('print_receipt.html', orders=orders, max_tables=max_tables)

if __name__ == '__main__':
    app.run(debug=True)
