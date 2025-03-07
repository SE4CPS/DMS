from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
DATABASE_URL = "water-run-comp163.c9qsek28w0ok.us-east-2.rds.amazonaws.com"
DB_USER = "team_1_COMP163"
DB_PASSWORD = "COMP163WaterRun"
DB_NAME = "water_run_COMP163"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return render_template('flowers.html')
    '''
    <h2>Flower Shop Management</h2>
    <button onclick="location.href='/flowers'">Manage Flowers</button>
    <button onclick="location.href='/customers'">Manage Customers</button>
    <button onclick="location.href='/orders'">Manage Orders</button>
    '''

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
