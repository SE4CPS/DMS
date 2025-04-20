import sqlite3
import psycopg2
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, redirect, url_for 

app = Flask(__name__)

# Database connection details
# DB_FILE = 'team-10.db'
DB_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

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
    cur.execute("UPDATE team10_flowers SET {} = ? WHERE name = ?".format(update_field), ( update_value, name))
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('index'))



@app.route('/remove_flower', methods=['POST'])
def delete_flower():
    name = request.form['name']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team10_flowers WHERE name = ?", (name,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/slow_query', methods=['POST'])
def slow_query():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
            """
            SELECT
            id,
            customer_id,
            flower_id
            FROM
            team10_orders
            FULL JOIN team10_customers ON team10_orders.customer_id=team10_customers.id
            FULL JOIN team10_flowers ON team10_orders.flower_id=team10_flowers.id
            ORDER BY team10_customers.name DESC;
            """
        )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

slow_query()

if __name__ == "__main__":
    app.run(debug=True)
