from flask import Flask, render_template, request, redirect
import psycopg2
from datetime import datetime
import time

app = Flask(__name__)
DATABASE_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return redirect('/team2_flowers')

@app.route('/team2_flowers', methods=['GET'])
def manage_flowers():
    print("Rendering team2_flowers.html")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team2_flowers")
    flowers = cur.fetchall()

    flowers_with_status = []
    for flower in flowers:
        id, name, last_watered, water_level, min_water_required, max_water_required = flower
        if water_level < min_water_required:
            water_status = "Needs Water💧"
        elif water_level == min_water_required:
            water_status = "Healthy ✅"
        else:
            water_status = "Overwatered 🚨"
        flowers_with_status.append((id, name, last_watered, water_level, min_water_required, max_water_required, water_status))
  
    cur.close()
    conn.close()
    return render_template('team2_flowers.html', flowers=flowers_with_status)

@app.route('/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    last_watered = request.form['last_watered']
    water_level = int(request.form['water_level'])
    min_water_required = int(request.form['min_water_required'])
    max_water_required = int(request.form['max_water_required'])

    if water_level < 0 or min_water_required < 0:
        raise ValueError("Water level and minimum water required must be positive integers")
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO team2_flowers (name, last_watered, water_level, min_water_required, max_water_required) VALUES (%s, %s, %s, %s, %s)",
                (name, last_watered, water_level, min_water_required, max_water_required))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/team2_flowers')

@app.route('/delete_flower/<int:flower_id>', methods=['POST'])
def delete_flower(flower_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team2_flowers WHERE id = %s", (flower_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/team2_flowers')

@app.route('/water_flowers', methods=['POST'])
def water_flower():
    # Gets flower ID
    flower_id = int(request.form['flower_id'])
    # Get the new water level
    new_water_level = int(request.form['water_level'])
    # gets current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("UPDATE team2_flowers SET water_level = %s, last_watered = %s WHERE id = %s", (new_water_level, current_date, flower_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/team2_flowers')

@app.route('/team2_flowers_water_loss', methods=['POST'])
def water_loss():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Run the SQL update query to decrease the water level
        cur.execute("""
            UPDATE team2_flowers
            SET water_level = water_level - (5 * (CURRENT_DATE - last_watered))
        """)
        conn.commit()
        print("Water levels updated successfully.")
    except Exception as e:
        print(f"Error updating water levels: {e}")
    finally:
        cur.close()
        conn.close()

    return redirect('/team2_flowers') 

@app.route('/slow_query')
def slow_query():
    conn = get_db_connection()
    cur = conn.cursor()

    slow_query_sql =  """
    SELECT 
        c.name,
        c.email,
        o.id AS order_id,
        f.name AS flower_name,
        f.water_level,
        (f.max_water_required - f.water_level) AS water_needed,
        EXTRACT(EPOCH FROM (NOW() - f.last_watered))/3600 AS hours_since_watering,
        CASE 
            WHEN f.water_level < f.min_water_required THEN 'Needs water'
            ELSE 'Healthy'
        END AS water_status
    FROM 
        team2_customers c
    JOIN 
        team2_orders o ON c.id = o.customer_id
    JOIN 
        team2_flowers f ON o.flower_id = f.id
    WHERE 
        o.order_date BETWEEN '2023-01-01' AND '2025-04-20'
        AND (SELECT COUNT(*) FROM generate_series(1,25000)) > 0 
        AND f.water_level < f.max_water_required
    ORDER BY 
        (SELECT COUNT(*) FROM team2_orders WHERE customer_id = c.id) DESC,
        hours_since_watering DESC,
        (SELECT COUNT(*) FROM team2_orders WHERE flower_id = f.id) DESC
    LIMIT 300;
    """

    start_time = time.time()
    cur.execute(slow_query_sql)
    execution_time = time.time() - start_time
    
    cur.close()
    conn.close()
    
    return render_template('query_results.html',
                         query_type="Slow Query (15-20s Target)",
                         query=slow_query_sql,
                         execution_time=execution_time)

if __name__ == '__main__':
    app.run(debug=True)