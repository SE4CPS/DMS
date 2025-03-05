from flask import Flask, render_template, request, redirect
import psycopg2
import datetime

app = Flask(__name__)
DATABASE_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True  # Enable auto-commit for transactions
    print("Connected to PostgreSQL successfully!")

    # Create a cursor object
    cur = conn.cursor()

# --- CREATE TABLES ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS team4_flowers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            last_watered DATE NOT NULL,
            water_level INT NOT NULL,
            min_water_required INT NOT NULL
        );
    """)

    # Creates the table with sample data if empty
    cur.execute("SELECT COUNT(*) FROM team4_flowers;")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("""
            INSERT INTO team4_flowers (name, last_watered, water_level, min_water_required)
            VALUES
            ('Rose', '2025-03-05', 20, 10),
            ('Lily', '2025-03-05', 4, 5),
            ('Tulip', '2025-03-05', 10, 8);
        """)
        print("Sample data inserted.")
    else:
        print("Sample data already exists.")

except Exception as e:
    print("Error:", e)

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    # Set Timezone for every new connection as well
    with conn.cursor() as cur:
        cur.execute("SET TIMEZONE = 'America/Los_Angeles';")  # Change timezone to match CURRENT_DATE timezone
    return conn

@app.route('/')
def index():
    return render_template('flowers.html')

# --- Main Structure --- #
@app.route('/flowers')
def flowers():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, last_watered, water_level, min_water_required FROM team4_flowers")
    flowers = cur.fetchall()
    
    # Convert fetched data into dictionaries
    formatted_flowers = []
    for flower in flowers:
        formatted_flowers.append({
            "id": flower[0],
            "name": flower[1] if flower[1] else "Unnamed",
            "last_watered": flower[2].strftime("%Y-%m-%d") if isinstance(flower[2], datetime.date) else "Unknown",
            "water_level": flower[3] if flower[3] is not None else 0,
            "min_water_required": flower[4] if flower[4] is not None else 0
        })
    
    cur.close()
    conn.close()
    
    return render_template('flowers.html', flowers=formatted_flowers)

# Get all Flowers
@app.route('/flowers')
def manage_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team4_flowers")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers.html', flowers=flowers)

# Add Flower
@app.route('/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    last_watered = request.form['last_watered']
    water_level = request.form['water_level']
    min_water_required = request.form['min_water_required']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO team4_flowers (name, last_watered, water_level, min_water_required) VALUES (%s, %s, %s, %s)", (name, last_watered, water_level, min_water_required))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

# Update Flower
@app.route('/update_flower/<int:flower_id>', methods=['POST'])
def update_flower(flower_id):
    name = request.form['name']
    last_watered = request.form['last_watered']
    water_level = request.form['water_level']
    min_water_required = request.form['min_water_required']

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE team4_flowers 
        SET name = %s, last_watered = %s, water_level = %s, min_water_required = %s 
        WHERE id = %s
    """, (name, last_watered, water_level, min_water_required, flower_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/flowers')

# Delete Flower
@app.route('/delete_team4_flower/<int:flower_id>', methods=['POST'])
def delete_flower(flower_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team4_flowers WHERE id = %s", (flower_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

# Water Loss Algorithm
@app.route('/simulate_water_loss')
def simulate_water_loss():
    print("Simulating water loss...")  # Debugging
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Debugging the number of days
        cur.execute("SELECT id, last_watered FROM team4_flowers")
        flowers = cur.fetchall()
        for flower in flowers:
            flower_id, last_watered = flower
            # Calculate the difference between the current date and last watered date
            date_diff = (datetime.date.today() - last_watered).days
            print(f"Flower ID: {flower_id}, Last Watered: {last_watered}, Days Diff: {date_diff}")

        cur.execute("""
                UPDATE team4_flowers
                SET water_level = water_level - (5 * (CURRENT_DATE - last_watered)),
                last_watered = CURRENT_DATE
        """)
        conn.commit()
    except Exception as e:
        print("Error updating water levels:", e)
    finally:
        cur.close()
        conn.close()
    return redirect('/flowers')

# -- Reset the Database ID to 1 (Testing purpose ONLY)
@app.route('/reset_flower_ids')
def reset_flower_ids():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team4_flowers")  # Deletes all records
    cur.execute("ALTER SEQUENCE team4_flowers_id_seq RESTART WITH 1")  # Resets ID
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

if __name__ == '__main__':
    app.run(debug=True)
