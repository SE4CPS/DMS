import random
from flask import Flask, render_template, request, redirect
import psycopg2
from datetime import timedelta, date
import datetime
import time
from faker import Faker

fake = Faker()  # Initialize Faker - Project 2

app = Flask(__name__)
DATABASE_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True  # Enable auto-commit for transactions
    print("Connected to PostgreSQL successfully!")

    # Create a cursor object
    cur = conn.cursor()

    # Ensure the 'water_added' column exists, if not add it
    cur.execute("""
        ALTER TABLE team4_flowers 
        ADD COLUMN IF NOT EXISTS water_added INT DEFAULT 0;
    """)

    # --- CREATE TABLES ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS team4_flowers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            last_watered DATE NOT NULL,
            water_level INT NOT NULL,
            min_water_required INT NOT NULL,
            water_added INT NOT NULL DEFAULT 0
        );
    """)

    # Creates the customers table - Project 2
    cur.execute("""
        CREATE TABLE IF NOT EXISTS team4_customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        );
    """)

    # Creates the orders table - Project 2
    cur.execute("""
        CREATE TABLE IF NOT EXISTS team4_orders (
            id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES team4_customers(id),
            flower_id INT REFERENCES team4_flowers(id),
            order_date DATE
        );
    """)

     # --- INDEXES FOR PERFORMANCE OPTIMIZATION ---
    cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON team4_orders(customer_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_flower_id ON team4_orders(flower_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_customers_id ON team4_customers(id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_flowers_id ON team4_flowers(id);")
    

    # Insert 100,000 customers if not already inserted - Project 2
    cur.execute("SELECT COUNT(*) FROM team4_customers;")
    customer_count = cur.fetchone()[0]
    if customer_count == 0:
        print("Inserting 100,000 customers...")
        for i in range(100000):
            # Using the Faker library to create realisitc data
            name = fake.name()
            email = fake.unique.email()
            cur.execute("INSERT INTO team4_customers (name, email) VALUES (%s, %s)", (name, email))
        print("Customer data inserted.")
    else:
        print(f"Already {customer_count} customers in the database.")

    # Insert 500,000 orders if not already inserted
    cur.execute("SELECT COUNT(*) FROM team4_orders;")
    order_count = cur.fetchone()[0]
    if order_count == 0:
        print("Inserting 500,000 orders...")
        for i in range(500000):
            customer_id = random.randint(1, 100000)
            flower_id = random.randint(1, 3)
            days_ago = random.randint(0, 365)
            cur.execute("""
                INSERT INTO team4_orders (customer_id, flower_id, order_date)
                VALUES (%s, %s, CURRENT_DATE - INTERVAL '%s days')
            """, (customer_id, flower_id, days_ago))
        print(f"Inserted {i} orders so far... (customer_id={customer_id}, flower_id={flower_id}, days_ago={days_ago})")
        print("Order data inserted.")
    else:
        print(f"Already {order_count} orders in the database.")
    
    # Creates the table with sample data if empty
    cur.execute("SELECT COUNT(*) FROM team4_flowers;")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("""
            INSERT INTO team4_flowers (name, last_watered, water_level, min_water_required)
            VALUES
            ('Rose', '2025-03-05', 20, 5),
            ('Lily', '2025-03-05', 10, 7),
            ('Tulip', '2025-03-05', 3, 5);
        """)
        print("Sample data inserted.")
    else:
        print(f"Number of rows in team4_flowers table: {count}")
        print("Sample data already exists.")

except Exception as e:
    print("Error:", e)

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    # Set Timezone for every new connection as well
    with conn.cursor() as cur:
        cur.execute("SET TIMEZONE = 'America/Los_Angeles';")  # Change timezone to match CURRENT_DATE timezone
    return conn

@app.route('/')
def index():
    return render_template('flowers.html')

# --- Main Structure --- #
@app.route('/flowers')
def flowers():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, last_watered, water_level, min_water_required, water_added FROM team4_flowers by ORDER BY id ASC")
    flowers = cur.fetchall()
    
    today = datetime.date.today()
    formatted_flowers = []

    for flower in flowers:
        
        water_level = flower[3]
        min_water_required = flower[4]
        #water_added = flower[5]
        days_since_watered = (today - flower[2]).days

        if water_level >= min_water_required and days_since_watered <= 2:
            watering_status = 'Well-watered'
        elif water_level > 0 and water_level < min_water_required:
            watering_status = 'Needs Watering'
        elif water_level <= 0:
            watering_status = 'Severely Dehydrated'
        elif 3 <= days_since_watered <= 5:
            watering_status = 'Needs Watering'
        elif 6 <= days_since_watered <= 8:
            watering_status = 'Dry'
        else:
            watering_status = 'Severely Dehydrated'

    # Convert fetched data into dictionaries
        formatted_flowers.append({
            "id": flower[0],
            "name": flower[1] if flower[1] else "Unnamed",
            "last_watered": flower[2].strftime("%Y-%m-%d") if isinstance(flower[2], datetime.date) else "Unknown",
            "water_level": flower[3] if flower[3] is not None else 0,
            "min_water_required": flower[4] if flower[4] is not None else 0,
            "water_added" : flower[5] if flower[5] is not None else 0,
            "watering_status": watering_status
        })
    
    cur.close()
    conn.close()
    
    return render_template('flowers.html', flowers=formatted_flowers)

# Add Flower
@app.route('/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    last_watered = request.form['last_watered']
    water_level = request.form['water_level']
    min_water_required = request.form['min_water_required']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO team4_flowers (name, last_watered, water_level, min_water_required) VALUES (%s, %s, %s, %s)", (name, last_watered, water_level, min_water_required))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

# Update Flower
@app.route('/update_flower/<int:flower_id>', methods=['POST'])
def update_flower(flower_id):
    name = request.form['name']
    last_watered = request.form['last_watered']
    water_level = request.form['water_level']
    min_water_required = request.form['min_water_required']

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE team4_flowers 
        SET name = %s, last_watered = %s, water_level = %s, min_water_required = %s 
        WHERE id = %s
    """, (name, last_watered, water_level, min_water_required, flower_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/flowers')

# Delete Flower
@app.route('/delete_team4_flower/<int:flower_id>', methods=['POST'])
def delete_flower(flower_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team4_flowers WHERE id = %s", (flower_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

# Water Loss Algorithm
@app.route('/simulate_water_loss')
def simulate_water_loss():
    print("Simulating water loss...")  # Debugging
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Debugging the number of days
        cur.execute("SELECT id, last_watered FROM team4_flowers")
        flowers = cur.fetchall()
        for flower in flowers:
            flower_id, last_watered = flower
            # Calculate the difference between the current date and last watered date
            date_diff = (datetime.date.today() - last_watered).days
            print(f"Flower ID: {flower_id}, Last Watered: {last_watered}, Days Diff: {date_diff}")

        cur.execute("""
                UPDATE team4_flowers
                SET water_level = water_level - (5 * (CURRENT_DATE - last_watered)),
                last_watered = CURRENT_DATE
        """)
        conn.commit()
    except Exception as e:
        print("Error updating water levels:", e)
    finally:
        cur.close()
        conn.close()
    return redirect('/flowers')

# Water Flower
@app.route('/water_flower/<int:flower_id>', methods=['POST'])
def water_flower(flower_id):
    water_added = int(request.form['water_added'])

    # Get the current water level for the flower 
    # Only the water level column
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT water_level FROM team4_flowers WHERE id = %s", (flower_id,))
    flower = cur.fetchone()
    current_water_level = flower[0]

    # Update the water level
    new_water_level = current_water_level + water_added

    # Update the water_added column to track the water added
    cur.execute("""
        UPDATE team4_flowers 
        SET water_level = %s, water_added = water_added + %s, last_watered = CURRENT_DATE
        WHERE id = %s
    """, (new_water_level, water_added, flower_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/flowers')

# Slow Query - Project 2
@app.route('/slow_query')
def slow_query():
    slow_sql = """
        SELECT c.name, o.order_date, f.name AS flower_name
        FROM team4_orders o
        CROSS JOIN team4_customers c 
        CROSS JOIN team4_flowers f
        ORDER BY o.order_date DESC LIMIT 500000 
    """ # with the cartesian join and limit of 500,000 the query time is 10 sec

    start_time = time.time()
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(slow_sql)
    results = cur.fetchall()
    cur.close()
    conn.close()

    end_time = time.time()
    query_time = end_time - start_time
    formatted_time = f"{query_time:.4f}" # Format query_time to 4 decimal places
    return render_template("flowers.html",
                           flowers = [], # Empty list to not conflict with flower table
                           query_type = "Slow Query",
                           query = slow_sql.strip(),
                           time = formatted_time,
                           row_count = len(results))

# Fast Query 
@app.route('/fast_query')
def fast_query():
    fast_sql = """
        SELECT o.id, c.name AS customer_name, f.name AS flower_name, o.order_date
        FROM team4_orders o
        JOIN team4_customers c ON o.customer_id = c.id
        JOIN team4_flowers f ON o.flower_id = f.id
        LIMIT 10;
    """

    start_time = time.time()
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(fast_sql)
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    end_time = time.time()
    query_time = end_time - start_time
    formatted_time = f"{query_time:.4f}" # Format query_time to 4 decimal places
    return render_template("flowers.html",
                           flowers = [], # Prevents template errors during query-only view
                           query_type = "Fast Query",
                           query = fast_sql.strip(),
                           time = formatted_time,
                           row_count = len(results))

# -- Reset the Database ID to 1 (Testing purpose ONLY)
@app.route('/reset_flower_ids')
def reset_flower_ids():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team4_flowers")  # Deletes all records
    cur.execute("ALTER SEQUENCE team4_flowers_id_seq RESTART WITH 1")  # Resets ID
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

if __name__ == '__main__':
    app.run(debug=True)
