from flask import Flask, request, jsonify
from flask import render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'bike.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    bikes_to_add = [
        ('Mountain Bike', 'Off-road'),
        ('Road Bike', 'On-road'),
        ('Hybrid Bike', 'Hybrid'),
        ('BMX', 'Stunt'),
        ('Folding Bike', 'Portable')
    ]
    with app.app_context():
        db = get_db_connection()
        db.execute('''CREATE TABLE IF NOT EXISTS bikes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        type TEXT NOT NULL
                      );''')
        db.executemany('INSERT OR IGNORE INTO bikes (name, type) VALUES (?, ?)', bikes_to_add)
        db.commit()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/bikes', methods=['GET'])
def get_bikes():
    conn = get_db_connection()
    bikes = conn.execute('SELECT * FROM bikes').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in bikes])

@app.route('/add_bike', methods=['POST'])
def add_bike():
    new_bike = request.json
    conn = get_db_connection()
    conn.execute('INSERT OR IGNORE INTO bikes (name, type) VALUES (?, ?)',
                 (new_bike['name'], new_bike['type']))
    conn.commit()
    conn.close()
    return {'message': 'Bike added successfully'}, 200

@app.route('/update_bike/<int:id>', methods=['PUT'])
def update_bike(id):
    update_details = request.json
    conn = get_db_connection()
    conn.execute('UPDATE bikes SET name = ?, type = ? WHERE id = ?',
                 (update_details['name'], update_details['type'], id))
    conn.commit()
    conn.close()
    return {'message': 'Bike updated successfully'}, 200

@app.route('/delete_bike/<int:id>', methods=['DELETE'])
def delete_bike(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM bikes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return {'message': 'Bike deleted successfully'}, 200

@app.route('/delete_all_bikes', methods=['DELETE'])
def delete_all_bikes():
    conn = get_db_connection()
    conn.execute('DELETE FROM bikes')
    conn.commit()
    conn.close()
    return {'message': 'All bikes deleted successfully'}, 200

if __name__ == '__main__':
    init_db()  # Initialize the database, create table if not exists, and add bikes
    app.run(debug=True)