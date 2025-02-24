from flask import Flask, render_template, request, redirect
import psycopg2

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

# --- UPDATE Water Level ---
    #curr.execute("""()""")

except Exception as e:
    print("Error:", e)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return render_template('flowers.html')

@app.route('/flowers')
def manage_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team4_flowers")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers.html', flowers=flowers)

@app.route('/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    color = request.form['color']
    price = request.form['price']
    stock = request.form['stock']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO team4_flowers (name, color, price, stock) VALUES (%s, %s, %s, %s)", (name, color, price, stock))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

@app.route('/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team4_flowers WHERE flower_id = %s", (flower_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

if __name__ == '__main__':
    app.run(debug=True)
