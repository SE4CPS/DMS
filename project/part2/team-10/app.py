import sqlite3
import psycopg2
import re
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, redirect, url_for 

app = Flask(__name__)

# Database connection details
# DB_FILE = 'team-10.db'
DB_URL = "postgresql://neondb_owner:npg_K4PbdhY0oTuH@ep-sweet-river-a4g0qfek-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    return conn
    # return sqlite3.connect(DB_FILE)

@app.route('/')
def index():
    return render_template("flowers.html")

# Get all flowers
@app.route('/flowers', methods=['GET'])
def get_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team10_flowers;")  # Placeholder for SELECT query
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify([{
        "id": f[0], "name": f[1], "last_watered": f[2],
        "water_level": f[3], "needs_watering": f[3] < f[4]
    } for f in flowers])

@app.route('/flowers/needs_watering', methods=['GET'])
def get_flowers_needing_water():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team10_flowers WHERE(water_level < min_water_required);")  # Placeholder for SELECT query
    flowers = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{
        "id": f[0], "name": f[1], "last_watered": f[2].strftime("%Y-%m-%d"),
        "water_level": f[3], "needs_watering": f[3] < f[4]
    } for f in flowers])

# Add a flower
@app.route('/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    last_watered = request.form['last_watered']
    water_level = request.form['water_level']
    min_water_required = request.form['min_water_required']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO team10_flowers (name, last_watered, water_level, min_water_required) VALUES('{}', '{}', {}, {})".format(name, last_watered, water_level, min_water_required))  # Placeholder
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))


@app.route('/update_flower', methods=['POST'])
def update_flower():
    name = request.form['name']
    update_field = request.form['update_field']
    update_value = request.form['update_value']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE team10_flowers SET {} = '{}' WHERE name = '{}'".format(update_field, update_value, name))
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('index'))



@app.route('/remove_flower', methods=['POST'])
def delete_flower():
    name = request.form['name']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team10_flowers WHERE name = '{}'".format(name))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/slow_query', methods=['GET'])
def slow_query():
    query = """
        BEGIN;
        DROP INDEX IF EXISTS idx_customers_id;
        DROP INDEX IF EXISTS idx_orders_customer_id;
        DROP INDEX IF EXISTS idx_flowers_name;
        COMMIT;
        EXPLAIN ANALYZE
        SELECT *
        FROM team10_orders
        FULL JOIN team10_customers ON team10_orders.customer_id=team10_customers.id
        CROSS JOIN team10_flowers
        ORDER BY team10_flowers.name
        """

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
            query
    )

    rows = cur.fetchall()

    for row in rows:
        for item in row:
            if (re.search(".*Execution Time:.*", item)):
                match = re.search("[0-9]*\.[0-9]*", item);
                seconds = round(float(item[match.span()[0]:match.span()[1]]) / 1000, 3)
                print('Execution Time: ', seconds)

    cur.close()
    conn.close()
    return """
    <h1>Slow Query:</h1>
    <h2>Execution Time (from EXPLAIN ANALYZE):</h2>
    <h3>{}</h3>
    <h2>SQL:</h2>
    <h3>{}</h3>
    """.format(seconds, query)

@app.route('/fast_query', methods=['GET'])
def fast_query():
    # Define optimized query without JOIN to non-existent table
    query = """
        EXPLAIN ANALYZE
        SELECT o.id as order_id, c.id as customer_id, f.id as flower_id
        FROM team10_orders o
        INNER JOIN team10_customers c ON o.customer_id = c.id
        JOIN (SELECT id FROM team10_flowers LIMIT 10) f ON true
        LIMIT 1000
        """
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create indexes first - do this in a separate try/except block
    try:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_customers_id ON team10_customers(id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON team10_orders(customer_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_flowers_name ON team10_flowers(name)")
        conn.commit()
    except Exception as e:
        print(f"Index creation warning: {e}")
    
    # Execute the optimized query
    cur.execute(query)
    rows = cur.fetchall()
    seconds = 0
    for row in rows:
        for item in row:
            if isinstance(item, str) and (re.search(".*Execution Time:.*", item)):
                match = re.search("[0-9]*\.[0-9]*", item)
                seconds = round(float(item[match.span()[0]:match.span()[1]]) / 1000, 3)
                print('Execution Time: ', seconds)
    cur.close()
    conn.close()
    
    return """
    <h1>Fast Query:</h1>
    <h2>Execution Time (from EXPLAIN ANALYZE):</h2>
    <h3>{}</h3>
    <h2>SQL:</h2>
    <h3>{}</h3>
    """.format(seconds, query)

if __name__ == "__main__":
    app.run(debug=True)
