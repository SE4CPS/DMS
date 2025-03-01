from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
DATABASE_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return '''
    <h2>Flower Shop Management</h2>
    <button onclick="location.href='/flowers'">Manage Flowers</button>
    <button onclick="location.href='/customers'">Manage Customers</button>
    <button onclick="location.href='/orders'">Manage Orders</button>
    '''

@app.route('/flowers')
def manage_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team6_flowers")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers.html', flowers=flowers)

#(name, last_watered, water_level, min_water_required) VALUES ('Rose', '2025-02-27', 10, 100)
@app.route('/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    last_watered = request.form['last_watered']
    water_level = request.form['water_level']
    min_water_required = request.form['min_water_required']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO team6_flowers (name, last_watered, water_level, min_water_required) VALUES (%s, %s, %s, %s)", (name, last_watered, water_level, min_water_required))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

@app.route('/flowers/needs_watering', methods=['GET'])
def get_flowers_needing_water():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team6_flowers WHERE water_level < min_water_required ORDER BY last_watered ASC")  # Placeholder for SELECT query
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers.html', flowers=flowers)

@app.route('/update_flower', methods=['POST'])
def update_flower():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE team6_flowers SET water_level = water_level - (5 * (CURRENT_DATE - last_watered));", None)
        conn.commit()
        cur.close()
        conn.close()
    except:
        print("Check Failed")
    
    return redirect('/flowers')


# Delete a flower by ID
@app.route('/delete_flower', methods=['POST'])
def delete_flower():
    id = request.form['id']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team6_flowers WHERE id = %s;", (id,)) # Placeholder
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

if __name__ == '__main__':
    app.run(debug=True)
