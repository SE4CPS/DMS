import psycopg2
import json
from flask import Flask, render_template, request, jsonify
from datetime import date, timedelta
import random

app = Flask(__name__)

# Database connection details
DATABASE_URL = "postgresql://neondb_owner:npg_QuIm1wktTiV0@ep-nameless-base-aab6w7ti-pooler.westus3.azure.neon.tech/neondb?sslmode=require"
conn = psycopg2.connect(DATABASE_URL)
print("Connected to PostgreSQL successfully!")

@app.route('/table', methods=['GET'])
def get_flowers():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS team7_customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    ); """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS team7_orders (
        id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES team7_customers(id),
        flower_id INT REFERENCES team7_flowers(id),
        order_date DATE
    );""")

    print("Tables created successfully.")
    return jsonify({"message": "Tables added !"})



@app.route('/create_tables', methods=['GET'])
def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("DROP TABLE IF EXISTS team7_orders;")
        cur.execute("DROP TABLE IF EXISTS team7_customers;")
    
        # Create team7_customers
        cur.execute("""
            CREATE TABLE IF NOT EXISTS team7_customers (
                id SERIAL PRIMARY KEY,
                name BYTEA,
                email BYTEA
            );
        """)

        # Create team7_orders
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
        for i in range(1000):
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
        for i in range(1000):
            customer_id = random.randint(1, 1000)
            flower_id = random.randint(1, 5)  # Ensure you have at least 5 flowers
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


# Add a new flower
if __name__ == '__main__':
    app.run(debug=True)