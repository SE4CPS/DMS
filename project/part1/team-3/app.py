import psycopg2
from flask import Flask, request, jsonify, render_template
from database.db_connection import get_db_connection

app = Flask(__name__)

# Database connection details

# Route to serve HTML page
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')

# Get all flowers
@app.route('/flowers', methods=['GET'])
def get_flowers():
    try:
        try:
            update_flower()
            print("Update successfully! YAY!")
        except Exception as e:
            print(f"Update information failed: {e}")
            
    
        conn = get_db_connection()
        print(f"Database connection success!") # TEST

        cur = conn.cursor()
        cur.execute("SELECT flower_id, flower_name, last_watered, water_level, min_water_required FROM team3_flowers")  
        flowers = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify([{
            "id": f[0], "name": f[1], "last_watered": f[2].strftime("%Y-%m-%d"),
            "water_level": f[3], "needs_watering": f[3] < f[4]
        } for f in flowers])
    except Exception as e:
        print(f"Database connection failed: {e}")

# Get flower need water
@app.route('/flowers/needs_watering', methods=['GET'])
def get_flowers_needing_water():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT flower_id, flower_name, last_watered, water_level, min_water_required 
        FROM team3_flowers
        WHERE water_level < min_water_required
        """)  # Placeholder for SELECT query
    flowers = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{
        "id": f[0], "name": f[1], "last_watered": f[2].strftime("%Y-%m-%d"),
        "water_level": f[3], "needs_watering": f[3] < f[4]
    } for f in flowers])

# Add a flower  
# curl http://127.0.0.1:5000/flowers -X POST -H "Content-Type: application/json" -d '{"id":null, "flower_name":"ABC", "last_watered":"2025-03-21", "water_level":0, "min_water_required":5}'
@app.route('/flowers', methods=['POST'])
def add_flower():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO team3_flowers (flower_name, last_watered, water_level, min_water_required)
        VALUES (%s, %s, %s, %s)
        """, 
        (data['flower_name'], data['last_watered'], data['water_level'], data['min_water_required']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower added successfully!"})

# Update a flower informtation
@app.route('/updated_flowers_level/', methods=['GET'])
def update_flower():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE team3_flowers
        SET water_level = 
            CASE
                WHEN water_level = 0 THEN 0
                ELSE GREATEST(0, water_level - (5 * (CURRENT_DATE - last_watered)))
            END;
        """
        ) 
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower updated successfully!"})

# Delete a flower by ID
@app.route('/flowers/<int:id>', methods=['DELETE'])
def delete_flower(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM team3_flowers WHERE flower_id = %s
        """, (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower deleted successfully!"})  
  

if __name__ == '__main__':
    app.run(debug=True)