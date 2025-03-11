import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Database connection details
DATABASE_URL = "postgresql://neondb_owner:npg_QuIm1wktTiV0@ep-nameless-base-aab6w7ti-pooler.westus3.azure.neon.tech/neondb?sslmode=require"
conn = psycopg2.connect(DATABASE_URL)
print("Connected to PostgreSQL successfully!")

# Get all flowers
@app.route('/flowers', methods=['GET'])
def get_flowers():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM team7_flowers;")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify([{
        "id": f[0], "name": f[1], "last_watered": f[2].strftime("%Y-%m-%d"),
        "water_level": f[3], "needs_watering": f[3] < f[4]
    } for f in flowers])

@app.route('/flowers/needs_watering', methods=['GET'])
def get_flowers_needing_water():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM team7_flowers WHERE water_level < min_water_required;")
    flowers = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{
        "id": f[0], "name": f[1], "last_watered": f[2].strftime("%Y-%m-%d"),
        "water_level": f[3], "needs_watering": f[3] < f[4]
    } for f in flowers])

# Add a flower
@app.route('/flowers', methods=['POST'])
def add_flower():
    data = request.json
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO team7_flowers (name, last_watered, water_level, min_water_required) VALUES (%s, %s, %s, %s)", 
                (data['name'], data['last_watered'], data['water_level'], data['min_water_required']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower added successfully!"})

# Update a flower by ID
@app.route('/flowers/<int:id>', methods=['PUT'])
def update_flower(id):
    data = request.json
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("UPDATE team7_flowers SET last_watered=%s, water_level=%s WHERE id=%s", 
                (data['last_watered'], data['water_level'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower updated successfully!"})

# Delete a flower by ID
@app.route('/flowers/<int:id>', methods=['DELETE'])
def delete_flower(id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("DELETE FROM team7_flowers WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower deleted successfully!"})  