import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("team11_flowers.db")
    conn.row_factory = sqlite3.Row
    return conn

# Get all flowers
@app.route('/flowers', methods=['GET'])
def get_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team11_flowers;")
    flowers = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{
        "id": f["id"], 
        "name": f["name"], 
        "last_watered": f["last_watered"],
        "water_level": f["water_level"], 
        "needs_watering": f["water_level"] < f["min_water_required"]
    } for f in flowers])

# Get flowers that need watering
@app.route('/flowers/needs_watering', methods=['GET'])
def get_flowers_needing_water():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team11_flowers WHERE water_level < min_water_required;")  # Fetch only needy plants
    flowers = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{
        "id": f["id"], 
        "name": f["name"], 
        "last_watered": f["last_watered"],
        "water_level": f["water_level"], 
        "needs_watering": f["water_level"] < f["min_water_required"]
    } for f in flowers])

# Add a new flower
@app.route('/flowers', methods=['POST'])
def add_flower():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO team11_flowers (name, last_watered, water_level, min_water_required) VALUES (?, ?, ?, ?)",
                (data['name'], data['last_watered'], data['water_level'], data['min_water_required']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower added successfully!"})

# Update a flower's watering status
@app.route('/flowers/<int:id>', methods=['PUT'])
def update_flower(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE team11_flowers SET last_watered = ?, water_level = ? WHERE id = ?",
                (data['last_watered'], data['water_level'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower updated successfully!"})

# Delete a flower by ID
@app.route('/flowers/<int:id>', methods=['DELETE'])
def delete_flower(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team11_flowers WHERE id = ?", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)