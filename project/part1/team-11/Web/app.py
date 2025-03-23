import sqlite3
from flask import Flask, request, jsonify, render_template, redirect

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("../team11_flowers.db")
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------
# 1) HOMEPAGE ROUTE (UI)
# -----------------------
@app.route('/')
def index():
    """
    A simple homepage with buttons or links to navigate.
    """
    return '''
    <h2>Team 11 Flower Management System</h2>
    <p>Welcome! Choose a section below:</p>
    <button onclick="location.href='/flowers_ui'">Manage Flowers (UI)</button>
    <br><br>
    <!-- If you have other sections, link them here as well -->
    <button onclick="location.href='/flowers'">List Flowers (JSON)</button>
    '''

# -----------------------
# 2) UI ROUTES (HTML)
# -----------------------
@app.route('/flowers_ui', methods=['GET'])
def flowers_ui():
    """
    Displays an HTML page (flowers11.html) showing all flowers in a table
    and a form to add a new flower (server-side rendered).
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team11_flowers;")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers11.html', flowers=flowers)

@app.route('/add_flower_form', methods=['POST'])
def add_flower_form():
    """
    Handles the form submission from flowers11.html (not JSON).
    Inserts a new flower into the database.
    """
    name = request.form['name']
    last_watered = request.form['last_watered']
    water_level = request.form['water_level']
    min_water_required = request.form['min_water_required']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO team11_flowers (name, last_watered, water_level, min_water_required)
        VALUES (?, ?, ?, ?)
    """, (name, last_watered, water_level, min_water_required))
    conn.commit()
    cur.close()
    conn.close()

    # Redirect back to /flowers_ui so we see the new flower listed
    return redirect('/flowers_ui')

@app.route('/delete_flower_ui/<int:flower_id>')
def delete_flower_ui(flower_id):
    """
    Deletes a flower by ID (via a simple GET link in the UI).
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team11_flowers WHERE id = ?", (flower_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers_ui')

@app.route('/update_flower_ui/<int:flower_id>', methods=['GET'])
def update_flower_ui(flower_id):
    """
    Displays a form allowing the user to update some or all fields.
    If they leave a field empty, it keeps the old value in the database.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team11_flowers WHERE id = ?", (flower_id,))
    flower = cur.fetchone()
    cur.close()
    conn.close()

    if not flower:
        return f"No flower found with ID {flower_id}", 404

    # The form includes placeholders showing old data, but user can clear fields if desired
    return render_template('update_flower.html', flower=flower)

@app.route('/update_flower_form/<int:flower_id>', methods=['POST'])
def update_flower_form(flower_id):
    """
    Handles partial updates: if a field is submitted as blank, keep the old value.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch the old row from the DB
    cur.execute("SELECT * FROM team11_flowers WHERE id = ?", (flower_id,))
    old_data = cur.fetchone()

    if not old_data:
        cur.close()
        conn.close()
        return f"No flower found with ID {flower_id}", 404

    # Grab new form data. If the user left the field empty, keep the old data
    name_input = request.form.get('name', '').strip()
    name = name_input if name_input else old_data['name']

    last_watered_input = request.form.get('last_watered', '').strip()
    last_watered = last_watered_input if last_watered_input else old_data['last_watered']

    water_level_input = request.form.get('water_level', '').strip()
    water_level = water_level_input if water_level_input else old_data['water_level']

    min_water_input = request.form.get('min_water_required', '').strip()
    min_water_required = min_water_input if min_water_input else old_data['min_water_required']

    # Update the row
    cur.execute("""
        UPDATE team11_flowers
        SET name = ?,
            last_watered = ?,
            water_level = ?,
            min_water_required = ?
        WHERE id = ?
    """, (name, last_watered, water_level, min_water_required, flower_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/flowers_ui')

# ---------------------------------
# 3) JSON ENDPOINTS (API)
# ---------------------------------

# GET all flowers as JSON
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
        "min_water_required": f["min_water_required"],
        "needs_watering": f["water_level"] < f["min_water_required"]
    } for f in flowers])

# GET flowers that need watering (JSON)
@app.route('/flowers/needs_watering', methods=['GET'])
def get_flowers_needing_water():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team11_flowers WHERE water_level < min_water_required;")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        "id": f["id"],
        "name": f["name"],
        "last_watered": f["last_watered"],
        "water_level": f["water_level"],
        "min_water_required": f["min_water_required"],
        "needs_watering": f["water_level"] < f["min_water_required"]
    } for f in flowers])

# POST (Add a new flower) via JSON
@app.route('/flowers', methods=['POST'])
def add_flower():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO team11_flowers (name, last_watered, water_level, min_water_required) VALUES (?, ?, ?, ?)",
        (data['name'], data['last_watered'], data['water_level'], data['min_water_required'])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower added successfully!"})

# PUT (Update a flower's watering status) via JSON
@app.route('/flowers/<int:id>', methods=['PUT'])
def update_flower(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE team11_flowers SET last_watered = ?, water_level = ? WHERE id = ?",
        (data['last_watered'], data['water_level'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower updated successfully!"})

# DELETE (Delete a flower) via JSON
@app.route('/flowers/<int:id>', methods=['DELETE'])
def delete_flower(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team11_flowers WHERE id = ?", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower deleted successfully!"})

# ---------------------------------
# Entry Point
# ---------------------------------
if __name__ == '__main__':
    app.run(debug=True)
