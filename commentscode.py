
ye app.py wli file se ha


Your table cooked_orders may have a column called customer_session.

If it exists:

The system finds the latest session for that table

And prints only those orders

This gives a correct receipt

If the column does NOT exist:

The system assumes all orders belong to the current people

(This is “legacy mode”)




    max_tables = fac_info[0][0] if fac_info else 50
    ye upr facinfo jaha aya ha wha table ki info ayi ha [(20,)] ase kr k
fac_info = [(20,)]
fac_info[0] = (20,) → first row
fac_info[0][0] = 20 → first column of first row → the number of tables




create-order.html me srf script mtlb js lgi ha or ha b nhi frontend me b srf add product and remove product
create-order.html me srf table number wla kam ha or phr scripts.js wli file me chla jata or product html wgra b wha hi add kr rha ha
script scripts.js bht easy ha agr ak br dkho to smjao ge is me dynamic html b isi js me add kr rhe ha jb add product click krte ha create order k wqt phr wo list me add hoti ha rhti or sth hi update status ka b fun ha jis me hm srf dynamically html k div ko target kr k ordered colour or choosing ka color change kr rhe ha or delete row b scripts.js wli file me hi



new_id = (last[0][0] or 0) + 1
last comes from a query like: SELECT MAX(id) FROM menu_config
The result is a list of rows, each row is a tuple, e.g. [(5,)] if max id = 5
last[0] → first row → (5,)




SELECT DISTINCT table_num ...

SELECT DISTINCT table_num → selects unique table numbers from the orders table.

ORDER BY table_num → sorts the table numbers in ascending order.




create-order.html me 
const menuItems = {{ menu_items | map(attribute=0) | list | tojson | safe }};
menu_items → a Python list of tuples from the database. Example:
python
Copy code
menu_items = [(‘Pizza’, 10), (‘Burger’, 5)]
map(attribute=0) → takes first element of each tuple → [‘Pizza’, ‘Burger’]
list → ensures it’s a Python list
tojson → converts it to JSON for JS → ["Pizza","Burger"]
safe → prevents Jinja from escaping quotes




product_name = html.escape(request.form.get('product_name', '').strip())
Meaning:
Gets the product_name from form
Removes extra spaces (strip())
Makes it safe for HTML (html.escape())
Example: user types <Soup> → becomes &lt;Soup&gt;




app.py me flash("message here written")
Aapke index.html (ya jis template me aap dikhana chahte ho) me ye block hona chahiye:
{% with messages = get_flashed_messages() %}
  {% if messages %}
    {% for msg in messages %}
      <div class="alert alert-info">{{ msg }}</div>
    {% endfor %}
  {% endif %}
{% endwith %}
⚠️ Agar ye block HTML me nahi hoga
➡️ Flash message kabhi display nahi hoga




These lines insert default values, but only if they do not already exist:
     db.insert_genconfig()
      def insert_genconfig(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS gen_config (id INTEGER PRIMARY KEY, conf_name text);")
         
            cursor.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)", (1, "fac_config"))
            cursor.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)", (2, "menu_config"))
            cursor.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)", (3, "orders"))
            conn.commit()
            conn.close()
            print("✅ Default config records inserted or already exist.")
        except Error as e:
            print("❌ Error inserting default configs:", e)
            
    
    
    
    
    
    
config.html me form tag ha dkh skte ho nche or ak input me hidden ha mtlb auto send id to backend server    
    Suppose you have a table of menu items, each with a Delete button.
You want to tell the server which item to remove without showing the ID to the user:
<form method="POST">
    <input type="hidden" name="remove_id" value="{{ item[0] }}">
    <button type="submit">Delete</button>
</form>
When the form is submitted, Flask receives:
remove_id = request.form.get('remove_id')
db.delete_val("DELETE FROM menu_config WHERE id=?", (remove_id,))
    
    
    
    
    
    
    
base.html khud se nahi chalta.
Woh tabhi chalta hai jab koi aur template usko extend kare using:
{% extends "base.html" %}
    
    
    round(2) mtlb . point k bd srf 2 digit ho
                    <td>{{ item[2] | float | round(2) }}</td>  
    
    
base.html me message flash wla code wo jo jitne b flash msg arhe ha yha se show ho rhe ha base.html me mtlb layout me     
Display message box
<div class="container flash-messages">
This creates a section on the page where messages will appear.
4️⃣ Loop through all messages
{% for message in messages %}
Agar 1 ya 5 messages hain → sab display honge.    
Why this block is inside base.html?
5️⃣ Show each message in Bootstrap alert style
<li class="list-group-item list-group-item-danger">{{ message }}</li>


list-group-item-danger → red background
Meaning: error message style
So that every page (index, kitchen, orders, config, etc.)
automatically shows flash messages.
Isliye ye best practice hai:
👉 ek hi jagah (base.html) me flash display code rakhna    
    
    
    
    
    
    
app.route('/') app.py file me            
Answer:
fac_info[0][0] tabhi chalega jab table fac_config me pehle se data ho jaise:
id | fac_name       | table_num | seat_num
1  | "Royal Hotel"  | 12        | 48
Then query result:
[("Royal Hotel",)]
So first 0 = first row
Second 0 = that row’s first column (which is fac_name)
    
    
    
@app.route('/print_receipt', methods=['GET', 'POST'])
def print_receipt():

    # Read restaurant name and maximum number of tables from the database.
    # Query returns something like: [("My Restaurant", 20)]
    fac_info = db.read_val("SELECT fac_name, table_num FROM fac_config LIMIT 1")

    # Example fac_info:
    # fac_info = [("My Restaurant", 20)]
    
    # If fac_info exists:
    # restaurant_name = "My Restaurant"
    # Else fallback: "Restaurant"
    restaurant_name = fac_info[0][0] if fac_info else "Restaurant"

    # Extract max table number (2nd column)
    # Example: max_tables = 20
    max_tables = fac_info[0][1] if fac_info else 50

    # Store orders that will be displayed or printed
    orders = []

    # Check if the user submitted the form
    if request.method == 'POST':

        # Get table number from form input
        table_num = request.form.get('table_num')

        # Action can be "new_customer" or "print"
        action = request.form.get('action')

        # If user pressed "Start New Customer Session"
        if action == 'new_customer' and table_num:
            try:
                # Convert to integer: e.g., "4" → 4
                table_num = int(table_num)

                # Validate table number
                if table_num < 1 or table_num > max_tables:
                    flash(f'Table number must be between 1 and {max_tables}!')

                else:
                    # Delete old orders for this table to start fresh
                    db.delete_val("DELETE FROM cooked_orders WHERE table_num=?", (table_num,))

                    flash(f'New customer session started for Table {table_num}!')

                return redirect(url_for('print_receipt'))

            except ValueError:
                flash('Table number must be a valid integer!')

        # If table number exists for printing receipt
        if table_num:
            try:
                table_num = int(table_num)

                # Validate
                if table_num < 1 or table_num > max_tables:
                    flash(f'Table number must be between 1 and {max_tables}!')

                else:
                    # Connect directly to SQLite to inspect the table structure
                    conn = sqlite3.connect('restaurant.db')
                    cursor = conn.cursor()

                    # PRAGMA tells SQLite to show metadata of columns
                    # Example result:
                    # [(0, 'id', ...), (1,'product_name'), (2,'order_quantity')]
                    cursor.execute("PRAGMA table_info(cooked_orders)")

                    # Extract only column names: ["id", "product_name", ...]
                    columns = [col[1] for col in cursor.fetchall()]

                    conn.close()

                    # Check if cooked_orders table has a column named "customer_session"
                    if 'customer_session' in columns:

                        # Get last session for this table
                        # Example: [[5]] means session 5
                        last_session = db.read_val(
                            "SELECT MAX(customer_session) FROM cooked_orders WHERE table_num=?", 
                            (table_num,)
                        )

                        # Extract session number or None
                        customer_session = (
                            last_session[0][0] 
                            if last_session and last_session[0][0] is not None
                            else None
                        )

                        # If session exists, load orders
                        if customer_session is not None:
                            # Query summarizes same product rows
                            orders = db.read_val("""
                                SELECT MIN(id) as id, product_name, SUM(order_quantity) as qty, SUM(order_price) as price
                                FROM cooked_orders 
                                WHERE table_num=? AND customer_session=?
                                GROUP BY product_name
                            """, (table_num, customer_session))

                        else:
                            # No orders found
                            orders = []

                    else:
                        # Legacy database without customer_session column
                        orders = db.read_val("""
                            SELECT MIN(id) as id, product_name, SUM(order_quantity) as qty, SUM(order_price) as price
                            FROM cooked_orders WHERE table_num=?
                            GROUP BY product_name
                        """, (table_num,))

                        # Legacy fallback
                        customer_session = 1

                    # If orders found, construct receipt HTML
                    if orders:

                        template_path = os.path.join(app.root_path, 'templates', 'order_template.html')

                        try:
                            with open(template_path, encoding='utf-8') as f:
                                soup = BeautifulSoup(f, 'html.parser')
                        except FileNotFoundError:
                            # Fallback HTML if template missing
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

                        # Replace placeholders
                        soup.find(text="Fac_name").replace_with(restaurant_name)
                        soup.find(text="t_num").replace_with(f"Table № {table_num}")

                        top_pad = 0
                        total_qty = 0
                        total_price = 0.0

                        # Loop through each order row
                        # Example order row:
                        # (5, "Burger", 2, 3000.00)
                        for order in orders:
                            name = order[1]
                            qty = order[2]
                            price = order[3]

                            total_qty += qty
                            total_price += price

                            # Create positioned elements
                            p_name = f"<span style='top:{150 + (top_pad * 20)}pt; left:85pt; position:absolute; font-size:20pt;'>{name}</span>"
                            p_qty = f"<span style='top:{150 + (top_pad * 20)}pt; left:275pt; position:absolute; font-size:20pt;'>x{qty}</span>"
                            p_price = f"<span style='top:{150 + (top_pad * 20)}pt; right:85pt; position:absolute; font-size:20pt;'>{price:.2f}</span>"

                            soup.div.append(BeautifulSoup(p_name, "html.parser"))
                            soup.div.append(BeautifulSoup(p_qty, "html.parser"))
                            soup.div.append(BeautifulSoup(p_price, "html.parser"))

                            top_pad += 1

                        # Draw horizontal line after last item
                        hr_style = f"top:{170 + (top_pad * 20)}pt;"
                        hr = f"<hr style='{hr_style}' />"

                        # Position total line
                        total_pos = 170 + (top_pad * 20) + 20
                        total = f"<span style='top:{total_pos}pt; left:85pt; position:absolute; font-size:20pt;'>Total ordered products: {total_qty}, total price: {total_price:.2f} ft</span>"

                        soup.div.append(BeautifulSoup(hr, "html.parser"))
                        soup.div.append(BeautifulSoup(total, "html.parser"))

                        # Save file as receipt_4_session_5.html
                        receipt_file = f"receipt_{table_num}_session_{customer_session or 'legacy'}.html"

                        with open(receipt_file, 'w', encoding='utf-8') as f:
                            f.write(str(soup))

                        # Open in browser
                        webbrowser.open('file://' + os.path.realpath(receipt_file))
                        flash('Receipt generated and opened for printing!')

                    else:
                        flash(f'No cooked orders found for table {table_num} in the current session!')

            except ValueError:
                flash('Table number must be a valid integer!')
            except sqlite3.OperationalError:
                flash('Database error while generating receipt. Please ensure database is updated.')
            except Exception:
                flash('Error generating receipt. Please try again.')

        else:
            flash('Please enter a table number!')

    # Return page with order list and max tables available
    return render_template('print_receipt.html', orders=orders, max_tables=max_tables)







=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================






@app.route('/kitchen', methods=['GET', 'POST'])
def kitchen():

    # If form is submitted (e.g., Mark Cooked or Fulfill Order button clicked)
    if request.method == 'POST':

        # Get which action user clicked: "mark_cooked" or "fulfill_order"
        action = request.form.get('action')
        # Example: action = "mark_cooked" OR action = "fulfill_order"

        # Get table number from form
        table_num = request.form.get('table_num')
        # Example: table_num = "4"

        # ------------------------------------------------------------
        # 1️⃣ MARK COOKED ACTION
        # ------------------------------------------------------------
        if action == 'mark_cooked':
            product_name = request.form.get('product_name')
            # Example: product_name = "Burger"

            if product_name and table_num:
                # Update the order status to "Cooked"
                db.update(
                    "UPDATE orders SET order_status='Cooked' WHERE table_num=? AND product_name=?", 
                    (table_num, product_name)
                )
                # Example SQL effect:
                # order_status changes from 'Ordered' → 'Cooked'

                flash('Item marked as cooked!')

        # ------------------------------------------------------------
        # 2️⃣ FULFILL ORDER ACTION (MOVE COOKED ITEMS TO cooked_orders TABLE)
        # ------------------------------------------------------------
        elif action == 'fulfill_order':
            if table_num:
                try:
                    table_num = int(table_num)
                    # Example: "4" → 4

                    # Read all COOKED items for this table
                    cooked = db.read_val(
                        "SELECT * FROM orders WHERE table_num=? AND order_status='Cooked'", 
                        (table_num,)
                    )
                    # Example cooked output:
                    # [
                    #   (5, 4, "Burger", 2, "Cooked"),
                    #   (6, 4, "Fries", 1, "Cooked")
                    # ]

                    if cooked:

                        # Try reading last session number from cooked_orders
                        try:
                            last_session = db.read_val(
                                "SELECT MAX(customer_session) FROM cooked_orders WHERE table_num=?", 
                                (table_num,)
                            )
                            # Example last_session output: [(3)] → last session = 3

                            customer_session = (
                                last_session[0][0] + 1  
                                if last_session and last_session[0][0] is not None  
                                else 1
                            )
                            # Example: New session = 4

                        except sqlite3.OperationalError as e:
                            # If column customer_session does NOT exist (old database)
                            if "no such column: customer_session" in str(e):
                                customer_session = 1  
                                # Always session 1 in old DB
                            else:
                                raise e

                        # ------------------------------------------------------------
                        # Move each COOKED order into cooked_orders table
                        # ------------------------------------------------------------
                        for order in cooked:
                            # Example order:
                            # order = (5, 4, "Burger", 2, "Cooked")

                            # Fetch price from menu_config
                            price_res = db.read_val(
                                "SELECT product_price FROM menu_config WHERE product_name=?", 
                                (order[2],)
                            )
                            # Example: price_res = [(1500)] ← 1500 per item

                            if price_res:
                                price = price_res[0][0]
                                # Example: price = 1500

                                total_price = order[3] * price
                                # Example: 2 × 1500 = 3000

                                # Get last used ID from cooked_orders to generate new ID
                                last_id = db.read_val(
                                    "SELECT id FROM cooked_orders ORDER BY id DESC LIMIT 1"
                                )
                                # Example: last_id = [(7)] → next id = 8

                                cooked_id = last_id[0][0] + 1 if last_id else 1

                                # Insert cooked order into cooked_orders table
                                try:
                                    db.insert_spec_config(
                                        "INSERT INTO cooked_orders VALUES (?, ?, ?, ?, ?, ?)", 
                                        (
                                            cooked_id,        # Example: 8
                                            order[1],         # table_num (4)
                                            order[2],         # product_name ("Burger")
                                            order[3],         # qty (2)
                                            total_price,      # 3000
                                            customer_session  # Example: 4
                                        )
                                    )

                                except sqlite3.OperationalError as e:
                                    # If old DB without customer_session column:
                                    if "no such column: customer_session" in str(e):
                                        db.insert_spec_config(
                                            "INSERT INTO cooked_orders (id, table_num, product_name, order_quantity, order_price) VALUES (?, ?, ?, ?, ?)", 
                                            (
                                                cooked_id,
                                                order[1],
                                                order[2],
                                                order[3],
                                                total_price
                                            )
                                        )
                                    else:
                                        raise e

                        # Remove cooked items from orders table
                        db.delete_val(
                            "DELETE FROM orders WHERE table_num=? AND order_status='Cooked'", 
                            (table_num,)
                        )
                        # Example: cooked items for table 4 removed from orders table

                        flash('Order fulfilled and moved to cooked orders!')

                    else:
                        flash('No cooked items to fulfill for this table!')

                except ValueError:
                    flash('Invalid table number!')

            return redirect(url_for('kitchen'))

    # ------------------------------------------------------------
    # Load all tables that currently have pending orders
    # ------------------------------------------------------------
    tables = db.read_val("SELECT DISTINCT table_num FROM orders ORDER BY table_num")
    # Example: [(1), (3), (4), (6)]

    orders_by_table = {}  
    has_ordered = {}

    for table in tables:
        table_num = table[0]

        # Group products by name & status
        orders = db.read_val("""
            SELECT MIN(id) as id, product_name, SUM(order_quantity) as qty, order_status
            FROM orders WHERE table_num=?
            GROUP BY product_name, order_status
        """, (table_num,))

        # Example orders output for table 4:
        # [
        #   (5, "Burger", 2, "Cooked"),
        #   (6, "Fries", 1, "Ordered")
        # ]

        orders_by_table[table_num] = orders

        # Check if any item is still in 'Ordered' state
        has_ordered[table_num] = any(o[3] == 'Ordered' for o in orders)
        # Example:
        # has_ordered[4] = True  (because "Fries" is Ordered)

    # Render the kitchen page with table order data
    return render_template(
        'kitchen.html', 
        orders_by_table=orders_by_table, 
        has_ordered=has_ordered
    )




=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================



@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    # Fetch all menu items from the database
    menu_items = db.read_val("SELECT product_name FROM menu_config")
    # Sample output: menu_items = [('Burger',), ('Pizza',), ('Pasta',)]

    # Fetch max table number from facility config
    fac_info = db.read_val("SELECT table_num FROM fac_config LIMIT 1")
    # Sample output: fac_info = [(20,)]

    # Set maximum allowed tables
    max_tables = fac_info[0][0] if fac_info else 50
    # Sample output: max_tables = 20

    # If no menu items configured, show warning
    if not menu_items:
        flash('Please configure menu items first in the Config page!')
        # Sample: user sees flash message in UI

    # Check if form is submitted
    if request.method == 'POST':
        # Get table number from form
        table_num = request.form.get('table_num')
        # Example: table_num = '3' (string from form)

        # Get selected products (list) from form
        products = request.form.getlist('product_name')
        # Example: products = ['Burger', 'Pizza']

        # Get quantities (list) from form
        quantities = request.form.getlist('quantity')
        # Example: quantities = ['2', '1']

        # Check if all required fields are filled
        if table_num and products and quantities:
            try:
                # Convert table number to integer
                table_num = int(table_num)
                # Example: table_num = 3

                # Validate table number range
                if table_num < 1 or table_num > max_tables:
                    flash(f'Table number must be between 1 and {max_tables}!')
                    return redirect(url_for('create_order'))
                    # Example flash if table_num=25, max_tables=20

                # Flag to check if all rows are valid
                valid = True
                # Loop through all products to validate selection and quantity
                for i, product in enumerate(products):
                    if product == '' or product == 'Select a meal':
                        flash('Please select a valid meal for all rows!')
                        valid = False
                        break
                        # Example: products = ['Burger', 'Select a meal'] → flash shown
                    try:
                        # Convert quantity to integer
                        quantities[i] = int(quantities[i])
                        # Example: quantities[i] = 2
                        # Check valid quantity range
                        if quantities[i] < 1 or quantities[i] > 100:
                            flash('Quantity must be between 1 and 100!')
                            valid = False
                            break
                            # Example: quantities[i] = 150 → flash shown
                    except ValueError:
                        flash('Quantity must be a valid number!')
                        valid = False
                        break
                        # Example: quantities[i] = 'abc' → flash shown

                # If all rows valid, insert into orders table
                if valid:
                    for i, product in enumerate(products):
                        if product != '' and product != 'Select a meal':
                            quantity = quantities[i]
                            # Get last order ID from database
                            last_id = db.read_val("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
                            # Sample: last_id = [(10,)]
                            # Calculate new order ID
                            order_id = last_id[0][0] + 1 if last_id else 1
                            # Example: order_id = 11
                            # Insert order into database
                            db.insert_spec_config(
                                "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
                                (order_id, table_num, product, quantity, 'Ordered')
                            )
                            # Example inserted row: (11, 3, 'Burger', 2, 'Ordered')

                    flash('Order sent to kitchen!')
                    # Example: user sees flash message
                    return redirect(url_for('create_order'))

            except ValueError:
                flash('Table number must be a valid number!')
                # Example: table_num = 'abc' → flash shown

        else:
            flash('Please fill all fields, including at least one product!')
            # Example: table_num = '', products=[] → flash shown

        return redirect(url_for('create_order'))

    # Render create_order page with menu items and max tables
    return render_template('create_order.html', menu_items=menu_items, max_tables=max_tables)
    # Example: page shows dropdown with menu_items = ['Burger', 'Pizza', 'Pasta'] and max_tables=20






=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================




@app.route('/config', methods=['GET', 'POST'])
def config():
    # Check if form is submitted
    if request.method == 'POST':
        # Get facility name from form, escape HTML and strip spaces
        fac_name = html.escape(request.form.get('fac_name', '').strip())
        # Example input: fac_name = "My Restaurant"

        # Get table number and seat number from form
        table_num = request.form.get('table_num')
        seat_num = request.form.get('seat_num')
        # Example input: table_num = '20', seat_num = '120'

        # Check if all facility fields are filled
        if fac_name and table_num and seat_num:
            try:
                # Convert table and seat numbers to integers
                table_num = int(table_num)
                seat_num = int(seat_num)
                # Example: table_num = 20, seat_num = 120

                # Validate maximum tables (cannot exceed 50)
                if table_num > 50:
                    flash('Maximum number of tables cannot exceed 50!')
                    # Example: table_num = 55 → flash shown

                # Validate maximum seats (cannot exceed table_num * 8)
                elif seat_num > (table_num * 8):
                    flash(f'Maximum number of seats cannot exceed {table_num * 8}!')
                    # Example: table_num = 20, seat_num = 200 → flash shown

                else:
                    # Check if facility config already exists
                    existing = db.read_val("SELECT * FROM fac_config")
                    # Example: existing = [(1, 'Old Restaurant', 15, 90)]

                    # Update existing facility config
                    if existing:
                        db.update("UPDATE fac_config SET fac_name=?, table_num=?, seat_num=? WHERE id=1", 
                                  (fac_name, table_num, seat_num))
                        # DB updated: ('My Restaurant', 20, 120)
                    # Insert new facility config if none exists
                    else:
                        db.insert_spec_config("INSERT INTO fac_config VALUES (?, ?, ?, ?)", 
                                              (1, fac_name, table_num, seat_num))
                        # DB inserted: (1, 'My Restaurant', 20, 120)

                    flash('Facility config saved!')
                    # Flash message shown in UI

            except ValueError:
                flash('Table and seat numbers must be valid integers!')
                # Example: table_num = 'abc' → flash shown

        # Get product name from form, escape HTML and strip spaces
        product_name = html.escape(request.form.get('product_name', '').strip())
        # Example input: product_name = "Burger"

        # Get product price from form
        product_price = request.form.get('product_price')
        # Example input: product_price = '150'

        # Check if both product fields are filled
        if product_name and product_price:
            try:
                # Convert product price to float
                product_price = float(product_price)
                # Example: product_price = 150.0

                # Validate product name length
                if len(product_name) > 20:
                    flash('Product name must be 20 characters or less!')
                    # Example: product_name = "VeryLongMealNameExceedingLimit"

                # Validate product price limit
                elif product_price > 10000000:
                    flash('Product price exceeds maximum allowed (10 million)!')
                    # Example: product_price = 20000000 → flash shown

                else:
                    # Check if product already exists
                    if db.read_val("SELECT id FROM menu_config WHERE product_name=?", (product_name,)):
                        flash('Product name already exists!')
                        # Example: 'Burger' already in DB

                    else:
                        # Get last product ID to assign new ID
                        last_id = db.read_val("SELECT id FROM menu_config ORDER BY id DESC LIMIT 1")
                        # Example: last_id = [(5,)]

                        # Calculate new product ID
                        pr_id = last_id[0][0] + 1 if last_id else 1
                        # Example: pr_id = 6

                        # Insert new product into menu_config
                        db.insert_spec_config("INSERT INTO menu_config VALUES (?, ?, ?)", 
                                              (pr_id, product_name, product_price))
                        # DB inserted: (6, 'Burger', 150.0)

                        flash('Product added!')
                        # Flash message shown in UI

            except ValueError:
                flash('Product price must be a valid number!')
                # Example: product_price = 'abc' → flash shown

        # Remove product if remove_id is provided
        remove_id = request.form.get('remove_id')
        # Example: remove_id = '3'
        if remove_id:
            db.delete_val("DELETE FROM menu_config WHERE id=?", (remove_id,))
            # DB row with id=3 deleted
            flash('Product removed!')
            # Flash message shown in UI

        # Redirect to refresh page after POST
        return redirect(url_for('config'))

    # For GET request: fetch existing facility config
    fac_config = db.read_val("SELECT * FROM fac_config LIMIT 1")
    # Example: fac_config = [(1, 'My Restaurant', 20, 120)]

    # Fetch all menu items
    menu_items = db.read_val("SELECT * FROM menu_config")
    # Example: menu_items = [(1, 'Burger', 150.0), (2, 'Pizza', 200.0)]

    # Render the config page with facility and menu info
    return render_template('config.html', 
                           fac_config=fac_config[0] if fac_config else None, 
                           menu_items=menu_items)
    # Page shows current facility config and menu items
