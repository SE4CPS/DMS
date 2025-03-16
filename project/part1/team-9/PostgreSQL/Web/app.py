import psycopg2
from flask import Flask, request, jsonify


app = Flask(__name__)
DATABASE_URL = "postgresql://flower_db_owner:npg_51HLIvYdpuVQ@ep-green-block-a8ifhr0o-pooler.eastus2.azure.neon.tech/flower_db?sslmode=require"

# Database connection details
def get_db_connection():
    return  psycopg2.connect(DATABASE_URL)

# Get all flowers
@app.route('/team9_flowers', methods=['GET'])
def get_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team9_flowers")  # This Query gets all of the flowers from the database
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify([{
        "id": f[0], "name": f[1], "last_watered": f[2].strftime("%Y-%m-%d"),
        "water_level": f[3], "needs_watering": f[3] < f[4]
    } for f in flowers])

@app.route('/team9_flowers/needs_watering', methods=['GET'])
def get_flowers_needing_water():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team9_flowers WHERE water_level < min_water_required")  # Placeholder for SELECT query
    flowers = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{
        "id": f[0], "name": f[1], "last_watered": f[2].strftime("%Y-%m-%d"),
        "water_level": f[3], "needs_watering": f[3] < f[4]
    } for f in flowers])

# Add a flower
@app.route('/add_team9_flowers', methods=['POST'])
def add_flower():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO team9_flowers (name, last_watered, water_level, min_water_required) VALUES (%s, %s, %s, %s)", 
                (data['name'], data['last_watered'], data['water_level'], data['min_water_required']))  # Placeholder
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower added successfully!"})

# Update a flower by ID
@app.route('/team9_flowers/<int:id>', methods=['PUT'])
def update_flower(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE team9_flowers SET last_watered = %s, water_level = %s WHERE id = %s", 
                (data['last_watered'], data['water_level'], id))  # Placeholder
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower updated successfully!"})

# Delete a flower by ID
@app.route('/team9_flowers/<int:id>', methods=['DELETE'])
def delete_flower(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team9_flowers WHERE id = %s", (id,))  # Placeholder
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower deleted successfully!"})  