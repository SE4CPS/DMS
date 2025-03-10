from flask import Flask, render_template, request, redirect
import psycopg2

# import postgress-crud.py into app.py
import postgress_crud as db

app = Flask(__name__)

# Flask route to display the home page
@app.route('/')
def index():
    return render_template('flowers.html')

@app.route('/flowers')
def manage_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flowerTest ")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers.html', flowers=flowers)

@app.route('/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    environment = request.form['environment']
    initial_water_level_in_inches = request.form['initial_water_level_in_inches']
    current_water_level_in_inches = initial_water_level_in_inches
    minimum_water_level_in_inches = request.form['minimum_water_level_in_inches']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO flowerTest (name, environment, initial_water_level_in_inches,  current_water_level_in_inches, minimum_water_level_in_inches) VALUES (%s, %s, %s, %s, %s)", (name, environment, initial_water_level_in_inches,  current_water_level_in_inches, minimum_water_level_in_inches))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

@app.route('/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM flowerTest WHERE flower_id = %s", (flower_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

if __name__ == '__main__':
    app.run(debug=True)
