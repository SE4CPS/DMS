import psycopg2
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Database connection details
DATABASE_URL = "postgresql://neondb_owner:npg_QuIm1wktTiV0@ep-nameless-base-aab6w7ti-pooler.westus3.azure.neon.tech/neondb?sslmode=require"
conn = psycopg2.connect(DATABASE_URL)
print("Connected to PostgreSQL successfully!")

# Get all flowers
@app.route('/', methods=['GET'])
def get_index():
    return render_template('flowers.html')

# Get all flowers
@app.route('/flowers', methods=['GET'])
def get_flowers():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM team7_flowers;")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    flowerJson = {}
    for flower in flowers:
        flowerJson[flower[0]] = {
            "name": flower[1],
            "last_watered": flower[2].strftime("%Y-%m-%d"),
            "water_level": flower[3],
            "min_water_required": flower[4]
        }
    return json.dumps(flowerJson)

# Add a new flower
if __name__ == '__main__':
    app.run(debug=True)