from flask import Flask, render_template, request, redirect, jsonify
import psycopg2
import sqlite3
import datetime
import time

app = Flask(__name__)
DATABASE_URL = "postgres://postgres:Sam123@localhost:5432/postgres"

def get_db_connection():
    return  psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return '''
    <h2>Flower Shop Management</h2>
    <button onclick="location.href='/flowers'">Manage Flowers</button>
    <button onclick="location.href='/customers'">Manage Customers</button>
    <button onclick="location.href='/orders'">Manage Orders</button>
    <button onclick="location.href='/slow_query'">Run Slow Query</button>
    <button onclick="location.href='/fast_query'">Run Fast Query</button>  
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
        last_date = last_watered
        since_watered = (c_date - last_date).days
        
        new_level = water_level - (5 * since_watered)
        if new_level < 0:
            new_level = 0
        
        cur.execute(f"""
            UPDATE team12_flowers
            SET water_level = %s
            WHERE name = %s
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

@app.route('/slow_query')
def slow_query():
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
            SELECT 
        o.id AS order_id,
        c.name AS customer_name,
        c.email,
        f.name AS flower_name,
        f.last_watered,
        f.water_level,
        f.min_water_required,
        o.order_date,
        LENGTH(o.encrypted_notes) AS note_length,
        (f.water_level - f.min_water_required) AS water_deficit,

        MD5(REPEAT(c.email || f.name, 75)) AS intense_hash,  
        LENGTH(REPEAT(c.name, 100)) AS long_name_calc,  
        LENGTH(REVERSE(REPEAT(o.encrypted_notes, 100))) AS reverse_load,  

        LOG(ABS(f.water_level * 1.5 + 100)) +
        SQRT(ABS(f.min_water_required * 1.25 + 200)) +
        EXP(ABS(f.water_level - f.min_water_required)) AS math_stuff, 

        REPEAT(f.name, 75) AS long_flower_name,  
        CONCAT(REPEAT(f.name, 100), REPEAT(c.name, 75)) AS concatenated_names,  

        
        COUNT(o.id) OVER() AS total_orders, 
        AVG(f.water_level) OVER(PARTITION BY f.name) AS avg_water_level,  

        
        (f.water_level * f.min_water_required) AS multiplication,
        (f.water_level + f.min_water_required) AS addition,
        (f.water_level / (f.min_water_required + 1)) AS division

    FROM team12_orders o
    JOIN team12_customers c ON o.customer_id = c.id
    JOIN team12_flowers f ON o.flower_id = f.id

    WHERE 
        LOWER(c.email) LIKE '%example.com'
        AND f.last_watered < CURRENT_DATE - INTERVAL '10 days'
        AND f.water_level < f.min_water_required
        AND LENGTH(o.encrypted_notes) > 30

    ORDER BY
        LENGTH(c.name) DESC,
        f.min_water_required DESC,
        o.order_date ASC

    LIMIT 5000;
    """
    
    conn = get_db_connection()
    cur = conn.cursor()

    start = time.time()
    cur.execute(query)
    cur.fetchall()  
    end = time.time()

    execution_time = round(end - start, 4)
    cur.close()
    conn.close()

    return render_template('slow.html', query=query, time=execution_time)

@app.route('/fast_query')
def fast_query():
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
                SELECT 
        o.id AS order_id,
        c.name AS customer_name,
        c.email,
        f.name AS flower_name,
        f.last_watered,
        f.water_level,
        f.min_water_required,
        o.order_date,
        LENGTH(o.encrypted_notes) AS note_length,
        (f.water_level - f.min_water_required) AS water_deficit
    FROM team12_orders o
    JOIN team12_customers c ON o.customer_id = c.id
    JOIN team12_flowers f ON o.flower_id = f.id
    WHERE 
        c.email ILIKE '%example.com'  
        AND f.last_watered < CURRENT_DATE - INTERVAL '10 days'
        AND f.water_level < f.min_water_required
        AND LENGTH(o.encrypted_notes) > 30
    ORDER BY
        o.order_date ASC  
    LIMIT 5000;
    """
    
    conn = get_db_connection()
    cur = conn.cursor()

    start = time.time()
    cur.execute(query)
    cur.fetchall()  
    end = time.time()

    execution_time = round(end - start, 4)
    cur.close()
    conn.close()

    return render_template('fast.html', query=query, time=execution_time)

if __name__ == '__main__':
    app.run(debug=True)