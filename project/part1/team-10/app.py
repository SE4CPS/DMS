import sqlite3
import psycopg2
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Database connection details
DB_FILE = 'team-10.db'

def get_db_connection():
    return sqlite3.connect(DB_FILE)

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
    return jsonify({"message": "Flower added successfully!"})

# Update a flower by ID
@app.route('/flowers/<int:id>', methods=['PUT'])
def update_flower(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE team10_flowers SET last_watered = {}, water_level = {} WHERE id = {};".format(data['last_watered'], data['water_level'], id))  # Placeholder
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower updated successfully!"})

# Delete a flower by ID
@app.route('/flowers/<int:id>', methods=['DELETE'])
def delete_flower(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team10_flowers WHERE id={};".format(id))  # Placeholder
    conn.commit()
    cur.close()
    conn.close()

print(sqlite3.connect(DB_FILE).cursor().execute('SELECT * FROM team10_flowers;').fetchall())

if __name__ == "__main__":
    app.run(debug=True)
