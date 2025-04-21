import psycopg2
import json
from flask import Flask, render_template, request, jsonify
import time
from datetime import date, timedelta, datetime
import random

app = Flask(__name__)

#testingifback
# Database connection details
DATABASE_URL = "postgresql://neondb_owner:npg_QuIm1wktTiV0@ep-nameless-base-aab6w7ti-pooler.westus3.azure.neon.tech/neondb?sslmode=require"

def get_db_connection():
    """Creates and returns a new database connection."""
    return psycopg2.connect(DATABASE_URL)

def update_water_levels():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE team7_flowers
        SET water_level = GREATEST(0, water_level - (5 * (CURRENT_DATE - last_watered)));
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Water levels updated")

'''
def set_test_last_watered():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE team7_flowers 
        SET last_watered = '2025-03-18'
        WHERE id = 10;
    """)  # You can change ID or apply it to all flowers if needed.
    conn.commit()
    cur.close()
    conn.close()
    print("set_test_last_watered")
'''

# Route to serve HTML page
@app.route('/', methods=['GET'])
def get_index():
    #set_test_last_watered()
    update_water_levels()
    print("set_test_last_watered")
    return render_template('flowers.html')

# Get all flowers
@app.route('/flowers', methods=['GET'])
def get_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team7_flowers;")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    
    flower_json = {
        flower[0]: {
            "id": flower[0],
            "name": flower[1],
            "last_watered": flower[2].strftime("%Y-%m-%d"),
            "water_level": flower[3],
            "min_water_required": flower[4]
        }
        for flower in flowers
    }
    return jsonify(flower_json)


# Add a new flower
@app.route('/flower', methods=['POST'])
def add_flower():
    data = request.json
    if not all(key in data for key in ['name', 'last_watered', 'water_level', 'min_water_required']):
        return jsonify({"error": "Missing required fields"}), 400

    # Ensure water_level and min_water_required are not negative
    water_level = max(data['water_level'], 0)
    min_water_required = max(data['min_water_required'], 0)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO team7_flowers (name, last_watered, water_level, min_water_required) VALUES (%s, %s, %s, %s) RETURNING id;",
        (data['name'], data['last_watered'], water_level, min_water_required)
    )
    new_id = cur.fetchone()[0]  # Get the newly inserted ID
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Flower added successfully!", "id": new_id})

'''

# Update water levels based on last watered date
@app.route('/needswater', methods=['GET'])
def get_flower_water():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Reduce water level based on days since last watered
    cur.execute("""
        UPDATE team7_flowers
        SET water_level = water_level - (5 * (CURRENT_DATE - last_watered));
    """)
    
    # Fetch flowers that need watering
    cur.execute("SELECT * FROM team7_flowers WHERE water_level < min_water_required;")
    flowers = cur.fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify([{
        "id": flower[0],
        "name": flower[1],
        "last_watered": flower[2].strftime("%Y-%m-%d"),
        "water_level": flower[3],
        "min_water_required": flower[4]
    } for flower in flowers])
'''

# Water a specific flower
@app.route('/water/<int:flower_id>', methods=['POST'])
def water_flower(flower_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Update last_watered to today and increase water level
    cur.execute("""
        UPDATE team7_flowers 
        SET last_watered = CURRENT_DATE, water_level = water_level + 10
        WHERE id = %s;
    """, (flower_id,))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": f"Flower {flower_id} watered successfully!"})


# **Update a flower by ID**
@app.route('/flowers/<int:id>', methods=['PUT'])
def update_flower(id):
    data = request.json
    if not all(key in data for key in ['last_watered', 'water_level']):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE team7_flowers 
        SET last_watered = %s, water_level = %s 
        WHERE id = %s;
    """, (data['last_watered'], data['water_level'], id))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": f"Flower {id} updated successfully!"})

# **Delete a flower by ID**
@app.route('/flowers/delete', methods=['DELETE'])
def delete_multiple_flowers():
    data = request.get_json()
    ids = data.get("ids", [])
    
    if not ids:
        return jsonify({"error": "No IDs provided"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    
 
    placeholders = ', '.join(['%s'] * len(ids))
    query = f"DELETE FROM team7_flowers WHERE id IN ({placeholders});"
    
    cur.execute(query, ids)
    conn.commit()
    
    deleted_count = cur.rowcount
    
    cur.close()
    conn.close()

    return jsonify({"message": f"{deleted_count} flowers deleted successfully."}), 200

@app.route('/slow', methods=['GET'])
def slow_query():
    start_time = time.time()
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Intentionally slow query: No LIMIT, inefficient order, decrypts everything
    cur.execute("""
        SELECT 
            o.id AS order_id,
            pgp_sym_decrypt(c.name, 'secret_key') AS customer_name,
            pgp_sym_decrypt(c.email, 'secret_key') AS customer_email,
            o.order_date
        FROM team7_orders o
        JOIN team7_customers c ON o.customer_id = c.id
        ORDER BY c.name DESC;
    """)
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    end_time = time.time()

    results = [{
        "order_id": row[0],
        "customer_name": row[1],
        "customer_email": row[2],
        "order_date": row[3].strftime("%Y-%m-%d")
    } for row in rows]

    return jsonify({
        "query_type": "slow",
        "duration_seconds": round(end_time - start_time, 4),
        "results": results[:10]
    })



@app.route('/fast', methods=['GET'])
def fast_query():
    start_time = time.time()
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # FAST: efficient join with LIMIT and only recent orders
    cur.execute("""
        SELECT 
            o.id AS order_id,
            pgp_sym_decrypt(c.name, 'secret_key') AS customer_name,
            pgp_sym_decrypt(c.email, 'secret_key') AS customer_email,
            o.order_date
        FROM team7_orders o
        JOIN team7_customers c ON o.customer_id = c.id
        ORDER BY o.order_date DESC
        LIMIT 10;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    end_time = time.time()

    results = [{
        "order_id": row[0],
        "customer_name": row[1],
        "customer_email": row[2],
        "order_date": row[3].strftime("%Y-%m-%d")
    } for row in rows]

    return jsonify({
        "query_type": "fast",
        "duration_seconds": round(end_time - start_time, 4),
        "results": results
    })




@app.route('/create_tables', methods=['GET'])
def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("DROP TABLE IF EXISTS team7_orders;")
        cur.execute("DROP TABLE IF EXISTS team7_customers;")

        # Create team7_customers table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS team7_customers (
                id SERIAL PRIMARY KEY,
                name BYTEA,
                email BYTEA
            );
        """)

        # Create team7_orders table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS team7_orders (
                id SERIAL PRIMARY KEY,
                customer_id INT REFERENCES team7_customers(id),
                flower_id INT REFERENCES team7_flowers(id),
                order_date DATE
            );
        """)

        conn.commit()
        message = "Tables created successfully!"
    except Exception as e:
        conn.rollback()
        message = f"Error: {str(e)}"
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": message})

@app.route('/populate_data', methods=['GET'])
def populate_data():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

        print("Inserting encrypted customers:")
        for i in range(10):
            name = f'Customer {i}'
            email = f'customer{i}@example.com'
            cur.execute("""
                INSERT INTO team7_customers (name, email)
                VALUES (
                    pgp_sym_encrypt(%s, 'secret_key'),
                    pgp_sym_encrypt(%s, 'secret_key')
                );
            """, (name, email))
            if i < 5:  # Only print the first few to avoid clutter
                print(f"Inserted customer {i}: {name}, {email}")

        print("\nInserting random orders:")
        for i in range(10):
            customer_id = random.randint(1, 10)
            flower_id = random.randint(1, 3)  # Ensure you have at least 5 flowers
            order_date = datetime.today() - timedelta(days=random.randint(0, 365))
            cur.execute("""
                INSERT INTO team7_orders (customer_id, flower_id, order_date)
                VALUES (%s, %s, %s);
            """, (customer_id, flower_id, order_date))
            if i < 5:  # Only print the first few to avoid too much output
                print(f"Inserted order {i}: Customer ID {customer_id}, Flower ID {flower_id}, Date {order_date}")

        conn.commit()
        message = "Inserted 1000 encrypted customers and 1000 orders"
    except Exception as e:
        conn.rollback()
        message = f"Error: {str(e)}"
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": message})



@app.route('/customers')
def get_customers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, 
               pgp_sym_decrypt(name, 'secret_key') AS name, 
               pgp_sym_decrypt(email, 'secret_key') AS email 
        FROM team7_customers 
        LIMIT 100;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    customers = [{'id': row[0], 'name': row[1], 'email': row[2]} for row in rows]
    return jsonify(customers)

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT * FROM team7_orders 
        LIMIT 100;
    """)
    
    orders = cur.fetchall()
    cur.close()
    conn.close()

    order_json = [
        {"id": row[0], "customer_id": row[1], "flower_id": row[2], "order_date": row[3].strftime("%Y-%m-%d")}
        for row in orders
    ]
    
    print("First 100 orders:")
    for order in order_json:
        print(order)

    return jsonify(order_json)



# Run the application
if __name__ == '__main__':
    app.run(debug=True)
