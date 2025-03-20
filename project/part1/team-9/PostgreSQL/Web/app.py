import psycopg2
from psycopg2 import OperationalError, DatabaseError
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

DATABASE_URL = "postgresql://flower_db_owner:npg_51HLIvYdpuVQ@ep-green-block-a8ifhr0o-pooler.eastus2.azure.neon.tech/flower_db?sslmode=require"

# Database connection details
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM team9_flowers;")
                flowers = cur.fetchall()
        return render_template('flowers.html', flowers=flowers) #Refers to our flowers.html file. 
    except (OperationalError, DatabaseError) as e:
        return jsonify({"error": str(e)}), 500

# Get all flowers
@app.route('/team9_flowers', methods=['GET'])
def get_flowers():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM team9_flowers;")
                flowers = cur.fetchall()
        return jsonify([{
            "id": f[0], 
            "name": f[1], 
            "last_watered": f[2].strftime("%Y-%m-%d"),
            "water_level": f[3], 
            "min_water_required": f[4]  # Ensure this is included
        } for f in flowers])
    except (OperationalError, DatabaseError) as e:
        return jsonify({"error": str(e)}), 500


# Add a flower
@app.route('/add_team9_flowers', methods=['POST'])
def add_flower():
    # Extract data from the incoming JSON request
    data = request.json
    name = data.get('name')
    last_watered = data.get('last_watered')
    water_level = data.get('water_level')
    min_water_required = data.get('min_water_required')

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO team9_flowers 
                    (name, last_watered, water_level, min_water_required) 
                    VALUES (%s, %s, %s, %s)
                """, (name, last_watered, water_level, min_water_required))
        return jsonify({"message": "Flower added successfully!"})
    except (OperationalError, DatabaseError) as e:
        return jsonify({"error": str(e)}), 500

# Update a flower by ID
@app.route('/team9_flowers/<int:id>', methods=['PUT'])
def update_flower(id):
    data = request.json
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE team9_flowers 
                    SET last_watered = %s, water_level = %s 
                    WHERE id = %s
                """, (data['last_watered'], data['water_level'], id))
        return jsonify({"message": "Flower updated successfully!"})
    except (OperationalError, DatabaseError) as e:
        return jsonify({"error": str(e)}), 500

# Delete a flower by ID
@app.route('/team9_flowers/<int:id>', methods=['DELETE'])
def delete_flower(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM team9_flowers WHERE id = %s", (id,))
        return jsonify({"message": "Flower deleted successfully!"})
    except (OperationalError, DatabaseError) as e:
        return jsonify({"error": str(e)}), 500
    
# New route to update the water levels
@app.route('/water_flowers', methods=['POST'])
def water_flowers():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE team9_flowers
                    SET water_level = water_level - (5 * (CURRENT_DATE - last_watered))
                    WHERE CURRENT_DATE > last_watered;
                """)
                conn.commit()  # Commit the transaction
        return jsonify({"message": "Water levels updated successfully!"})
    except (OperationalError, DatabaseError) as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)