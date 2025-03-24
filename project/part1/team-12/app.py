from flask import Flask, render_template, request, redirect, jsonify
#import psycopg2
import sqlite3
import datetime

app = Flask(__name__)
DATABASE_URL = "C://Users//smori//OneDrive//Desktop//Databases//DMS//project//part1//team-12//team12_flowers.db"

def get_db_connection():
    return sqlite3.connect(DATABASE_URL)

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
    c_date = datetime.datetime.now().date()
    cur.execute("SELECT * FROM team12_flowers;")
    flowers = cur.fetchall()
    for flower in flowers:
        blank, name, last_watered, water_level, min_level = flower
        last_date = datetime.datetime.strptime(last_watered, "%Y-%m-%d").date()
        since_watered = (c_date - last_date).days
        
        new_level = water_level - (5 * since_watered)
        if new_level < 0:
            new_level = 0
        
        cur.execute(f"""
            UPDATE team12_flowers
            SET water_level = ?
            WHERE name = ?
        """, (new_level, name))
    
        conn.commit()
        
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
    cur.execute("INSERT INTO team12_flowers (name, color, price, stock) VALUES (?, ?, ?, ?)", (name, color, price, stock))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

@app.route('/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team12_flowers WHERE flower_id = ?", (flower_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

if __name__ == '__main__':
    app.run(debug=True)