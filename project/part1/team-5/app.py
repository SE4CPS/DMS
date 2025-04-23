from flask import Flask, render_template, request, redirect,jsonify
import psycopg2

app = Flask(__name__)

DATABASE_URL = "postgresql://neondb_owner:npg_tRjAlmCi4y6n@ep-bold-lake-a5wpofnx-pooler.us-east-2.aws.neon.tech/dbms?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
   return '''
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
                text-align: center;
                padding-top: 50px;
            }
            h2 {
                color: #4CAF50;
                margin-bottom: 40px;
            }
            button {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 30px;
                margin: 10px;
                text-align: center;
                font-size: 16px;
                border-radius: 8px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <h2>Flower Shop Management</h2>
        <button onclick="location.href='/flowers'">Manage Flowers</button>
        <button onclick="location.href='/flowers/needs_watering'">Manage Water Levels</button>
    </body>
    </html>
    '''


# Get all flowers
@app.route('/flowers')
def manage_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team5_flowers")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers.html', flowers=flowers)

@app.route('/flowers/daily_loss', methods=['GET'])
def daily_water_loss():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id,name,last_watered,water_level FROM team5_flowers")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    flower_list = [
        {
            "id": flower[0],
            "name": flower[1],
            "last_watered": flower[2],
            "water_level": flower[3]
        } for flower in flowers
    ]
    return jsonify(flower_list)


# Get all flowers that need to be watered
@app.route('/flowers/needs_watering', methods=['GET'])
def get_flowers_needing_water():
    conn = get_db_connection()
    cur= conn.cursor()
    cur.execute("SELECT * FROM team5_flowers WHERE water_level < min_water_required")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('flowers.html', flowers=flowers)

# Add a new flower
@app.route('/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    last_watered = request.form['last_watered']
    water_level = request.form['water_level']
    min_water_required = request.form['min_water_required']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO team5_flowers (name, last_watered, water_level, min_water_required) VALUES (%s, %s, %s, %s)", (name, last_watered, water_level, min_water_required)) #protecting from SQL injection
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/flowers')

    # Update a flower water level by ID
@app.route('/flowers/<int:flower_id>', methods=['PUT'])
def update_flower(flower_id):
    data = request.json # Get the JSON data from the request
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE team5_flowers SET last_watered = %s, water_level = %s WHERE id = %s",
    (data['last_watered'], data['water_level'], flower_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower updated successfully!"})


@app.route('/delete_flower/<int:flower_id>', methods=['DELETE'])
def delete_flower(flower_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team5_flowers WHERE id = %s", (flower_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Flower deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)