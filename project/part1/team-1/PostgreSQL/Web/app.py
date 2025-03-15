from flask import Flask, render_template, request, redirect
import psycopg2, os, sys, datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# import postgress-crud.py into app.py
from PostgreSQL import postgress_crud as db

app = Flask(__name__)

# Flask route to display the home page
@app.route('/')
def index():
    return render_template('flowers.html')

# updating current_water_level_in_inches
def update_flowers():
    conn = db.get_db_connection()
    cur = conn.cursor()
    currDate = datetime.datetime.now()
    cur.execute("UPDATE flower SET current_water_level_in_inches = current_water_level_in_inches - (5 * (%s - last_watered)) WHERE flower_id IS NOT NULL", (currDate,))
    # cur.execute("UPDATE FROM flower SET current_water_level_in_inches = current_water_level_in_inches - (5 * (%s - last_watered))", (currDate))
    cur.close()
    conn.close()
    

@app.route('/flowers')
def manage_flowers():
    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flower")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers.html', flowers=flowers)

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
    cur.execute("INSERT INTO flower (name, environment, initial_water_level_in_inches,  current_water_level_in_inches, minimum_water_level_in_inches) VALUES (%s, %s, %s, %s, %s)", (name, environment, initial_water_level_in_inches,  current_water_level_in_inches, minimum_water_level_in_inches))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

# Deleting Flower Function
@app.route('/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM flower WHERE flower_id = %s", (flower_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')


# Watering Flower Function
@app.route('/water_flower/<int:flower_id>')
def water_flower(flower_id):
    conn = db.get_db_connection()
    cur = conn.cursor()
    currDate = datetime.datetime.now()
    #cur.execute("UPDATE FROM flower SET current_water_level_in_inches = current_water_level_in_inches + 5 WHERE flower_id = %s", (flower_id,))
    cur.execute("UPDATE flower SET current_water_level_in_inches = current_water_level_in_inches + 5 WHERE flower_id = %s", (flower_id,))
    cur.execute("UPDATE FROM flower SET last_watered = %s currDate WHERE flower_id = %s", (currDate,flower_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

# Retrieving flowers that need to be watered
@app.route('/needs_water')
def need_to_be_watered_flowers():
    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flower WHERE needs_water = TRUE")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers.html', flowers=flowers)

# Retrieving flowers that are outdoor
@app.route('/outdoor_water')
def outdoor_flowers():
    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flower WHERE environment = 'outdoor'")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers.html', flowers=flowers)

# Retrieving flowers that are indoor
@app.route('/indoor_water')
def indoor_flowers():
    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flower WHERE environment = 'indoor'")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers.html', flowers=flowers)



if __name__ == '__main__':
    app.run(debug=True)
