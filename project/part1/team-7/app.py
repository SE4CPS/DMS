import psycopg2
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Database connection details
DATABASE_URL = "postgresql://neondb_owner:npg_QuIm1wktTiV0@ep-nameless-base-aab6w7ti-pooler.westus3.azure.neon.tech/neondb?sslmode=require"

def get_db_connection():
    """Creates and returns a new database connection."""
    return psycopg2.connect(DATABASE_URL)

# Route to serve HTML page
@app.route('/', methods=['GET'])
def get_index():
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

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO team7_flowers (name, last_watered, water_level, min_water_required) VALUES (%s, %s, %s, %s) RETURNING id;",
        (data['name'], data['last_watered'], data['water_level'], data['min_water_required'])
    )
    new_id = cur.fetchone()[0]  # Get the newly inserted ID
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Flower added successfully!", "id": new_id})

# Update water levels based on last watered date
@app.route('/needswater', methods=['GET'])
def get_flower_water():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Reduce water level based on days since last watered
    cur.execute("""
        UPDATE team7_flowers 
        SET water_level = water_level - (5 * EXTRACT(DAY FROM (CURRENT_DATE - last_watered))) 
        WHERE water_level > 0;
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
@app.route('/flowers/<int:id>', methods=['DELETE'])
def delete_flower(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM team7_flowers WHERE id = %s;", (id,))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": f"Flower {id} deleted successfully!"})


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
