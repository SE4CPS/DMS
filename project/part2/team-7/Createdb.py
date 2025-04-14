import psycopg2
import json
from flask import Flask, render_template, request, jsonify

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


# Add a new flower
if __name__ == '__main__':
    app.run(debug=True)