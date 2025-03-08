from flask import Flask, render_template, request, redirect
import psycopg2

# import postgress-crud.py into app.py
import postgress_crud as db

app = Flask(__name__)

# Commented out the below code as it is already present in postgress-crud.py
'''
DATABASE_URL = "water-run-comp163.c9qsek28w0ok.us-east-2.rds.amazonaws.com"
DB_USER = "team_1_COMP163"
DB_PASSWORD = "COMP163WaterRun"
DB_NAME = "water_run_COMP163"
'''

# Database connect done in postgress-crud.py
'''
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)
'''

# Flask route to display the home page
@app.route('/')
def index():
    return render_template('flowers.html')

@app.route('/flowers')
def manage_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flowers")
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
    cur.execute("INSERT INTO flowers (name, color, price, stock) VALUES (%s, %s, %s, %s)", (name, color, price, stock))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

@app.route('/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM flowers WHERE flower_id = %s", (flower_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

if __name__ == '__main__':
    app.run(debug=True)
