from flask import Flask, render_template, request, redirect
import psycopg2, os, sys, datetime
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# import postgress-crud.py into app.py
from PostgreSQL import postgress_crud as db

app = Flask(__name__)

# Flask route to display the home page
@app.route('/')
def index():
    return render_template('flowers.html')

@app.route('/flowers')
def manage_flowers():
    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flower")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers.html', flowers=flowers)

# TO DO: Add a function to update the current water level in inches for each flower in the database based on the time since the last watering
def update_flowers():
    conn = db.get_db_connection()
    cur = conn.cursor()
    currDate = datetime.datetime.now()
    cur.execute("UPDATE flower SET current_water_level_in_inches = current_water_level_in_inches - (5 * (%s - last_watered)) WHERE flower_id IS NOT NULL", (currDate,))
    # cur.execute("UPDATE FROM flower SET current_water_level_in_inches = current_water_level_in_inches - (5 * (%s - last_watered))", (currDate))
    cur.close()
    conn.close()

# Adding Flower Function
@app.route('/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    environment = request.form['environment']
    initial_water_level_in_inches = request.form['initial_water_level_in_inches']
    current_water_level_in_inches = initial_water_level_in_inches
    minimum_water_level_in_inches = request.form['minimum_water_level_in_inches']
    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO flower (name, environment, initial_water_level_in_inches,  current_water_level_in_inches, minimum_water_level_in_inches,last_watered) VALUES (%s, %s, %s, %s, %s, %s)", (name, environment, initial_water_level_in_inches,  current_water_level_in_inches, minimum_water_level_in_inches,datetime.datetime.now()))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

# Watering Flower Function
@app.route('/water_flower')
def water_flowers():
    flowers = db.watering_flowers_helper()
    return render_template('water_flower.html', flowers=flowers)
    
@app.route('/water_flower', methods=['POST'])
def water_selected_flowers():
    conn = db.get_db_connection()
    cur = conn.cursor()
    selected_flowers = request.form.getlist('selected_flowers')
    for f in selected_flowers:
        flower_id = f.split(",")[0]
        flower_id = flower_id[1:]
        flower_id = int(flower_id)
        currDate = datetime.datetime.now()
        cur.execute("UPDATE flower SET current_water_level_in_inches = current_water_level_in_inches + 10 WHERE flower_id = %s", (flower_id,))
        cur.execute("UPDATE flower SET last_watered = %s WHERE flower_id = %s", (currDate,flower_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

# Query Functions
@app.route('/all_flower')
def all_flowers_query():
    flowers = db.manage_flowers()
    return render_template('all_flower.html', flowers=flowers)

@app.route('/needs_water')
def need_water_query():
    flowers = db.need_to_be_watered_flowers()
    return render_template('needs_water.html', flowers=flowers)

@app.route('/outdoor_flower')
def outdoor_flower_query():
    flowers = db.outdoor_flowers()
    return render_template('outdoor_flower.html', flowers=flowers)

@app.route('/indoor_flower')
def indoor_flower_query():
    flowers = db.indoor_flowers()
    return render_template('indoor_flower.html', flowers=flowers)

# Simulate Rainfall
@app.route('/simulate_rainfall')
def water_outdoor_flowers():
    flowers = db.manage_flowers()
    return redirect('/flowers')

# Remove specific flower(s)
@app.route('/remove_flower', methods=['GET', 'POST'])
def remove_flower():
    delete_flowers = []

    if request.method == 'POST':
        selected_flower_ids = request.form.getlist('selected_flowers')

        if selected_flower_ids:
            delete_flowers = db.remove_selected_flower(selected_flower_ids)

    flowers = db.manage_flowers()
    
    return render_template('delete_flower.html', flowers=flowers, delete_flowers=delete_flowers)

if __name__ == '__main__':
    app.run(debug=True)