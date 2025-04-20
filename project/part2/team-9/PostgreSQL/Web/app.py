import time # added 
import psycopg2
from psycopg2 import OperationalError, DatabaseError
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

DATABASE_URL = "postgresql://flower_db_owner:npg_51HLIvYdpuVQ@ep-green-block-a8ifhr0o-pooler.eastus2.azure.neon.tech/flower_db?sslmode=require"

# Database connection details
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM team9_flowers ORDER BY id;")
                flowers = cur.fetchall()
        return render_template('flowers.html', flowers=flowers) #Refers to our flowers.html file. 
    except (OperationalError, DatabaseError) as e:
        return jsonify({"error": str(e)}), 500

# Get all flowers and update water levels
@app.route('/team9_flowers', methods=['GET'])
def get_flowers():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Now fetch all flowers to display
                cur.execute("SELECT * FROM team9_flowers ORDER BY id;")
                flowers = cur.fetchall()
                
        return jsonify([{
            "id": f[0],
            "name": f[1],
            "last_watered": f[2].strftime("%Y-%m-%d"),
            "water_level": f[3],
            "min_water_required": f[4],
            "needs_water": f[3] < f[4]# Including the needs_water status
        } for f in flowers])
    except (OperationalError, DatabaseError) as e:
        return jsonify({"error": str(e)}), 500



@app.route('/add_team9_flowers', methods=['POST'])
def add_flower():
    # Extract data from the incoming JSON request
    data = request.json
    name = data.get('name')
    last_watered = data.get('last_watered')
    water_level = data.get('water_level')
    min_water_required = data.get('min_water_required')

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Insert the new flower and retrieve the id of the newly added flower
                cur.execute("""
                    INSERT INTO team9_flowers 
                    (name, last_watered, water_level, min_water_required) 
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (name, last_watered, water_level, min_water_required))

                # Fetch the id of the newly inserted flower
                new_flower_id = cur.fetchone()[0]

                # Now, update the water level for just the newly added flower
                cur.execute("""
                    UPDATE team9_flowers
                    SET water_level = water_level - (5 * (CURRENT_DATE - last_watered))
                    WHERE id = %s
                """, (new_flower_id,))

                conn.commit()  # Commit the transaction to insert the flower and update water level

        return jsonify({"message": "Flower added successfully!"})
    except (OperationalError, DatabaseError) as e:
        return jsonify({"error": str(e)}), 500


@app.route('/team9_flowers/<int:id>', methods=['PUT'])
def update_flower(id):
    data = request.json
    
    # Ensure we have the correct values
    if not data.get('last_watered') or not data.get('water_level'):
        return jsonify({"error": "Invalid input, 'last_watered' and 'water_level' are required."}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Log the id being updated and the data being used
                print(f"Updating flower with ID: {id}")
                print(f"New data: last_watered={data['last_watered']}, water_level={data['water_level']}")

                # Perform the update for last_watered and water_level
                cur.execute("""
                    UPDATE team9_flowers 
                    SET last_watered = %s, water_level = %s 
                    WHERE id = %s
                """, (data['last_watered'], data['water_level'], id))

                # Now, update the water_level based on the new last_watered date
                cur.execute("""
                    UPDATE team9_flowers
                    SET water_level = water_level - (5 * (CURRENT_DATE - last_watered))
                    WHERE id = %s
                """, (id,))  # Pass the specific id of the flower being updated

                conn.commit()  # Commit the transaction

        return jsonify({"message": "Flower updated successfully!"})
    except (OperationalError, DatabaseError) as e:
        return jsonify({"error": str(e)}), 500



# Delete a flower by ID
@app.route('/team9_flowers/<int:id>', methods=['DELETE'])
def delete_flower(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM team9_flowers WHERE id = %s", (id,))
        return jsonify({"message": "Flower deleted successfully!"})
    except (OperationalError, DatabaseError) as e:
        return jsonify({"error": str(e)}), 500

# Slow Query
@app.route('/slow_query')
def slow_query():
    start_time = time.time()  # Start timer
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                print('Running slow query...')

                # Dropping indexes for poor performance (as you intended)
                cur.execute("DROP INDEX IF EXISTS idx_orders_customer_id;")
                cur.execute("DROP INDEX IF EXISTS idx_orders_flower_id;")
                cur.execute("DROP INDEX IF EXISTS idx_customers_email;")
                cur.execute("DROP INDEX IF EXISTS idx_orders_order_date;")

                # Simulate expensive operations: joins, sorting, filtering, and encryption
                cur.execute("""
                    SELECT 
                        pgp_sym_encrypt(c.name, 'encryptionkey') AS encrypted_name,
                        pgp_sym_encrypt(c.email, 'encryptionkey') AS encrypted_email,
                        f.name AS flower_name,
                        o.order_date,
                        LENGTH(c.email),
                        UPPER(f.name)    
                    FROM team9_orders o
                    JOIN team9_customers c ON o.customer_id = c.id
                    JOIN team9_flowers f ON o.flower_id = f.id
                    WHERE o.order_date >= CURRENT_DATE - INTERVAL '365 days'
                    ORDER BY c.email, o.order_date DESC
                    LIMIT 100000;
                """)

                # Check if results are returned
                results = cur.fetchall()

                # Log the number of rows returned for debugging purposes
                print(f"Number of rows returned: {len(results)}")

        # Calculate and log the execution time
        execution_time = time.time() - start_time
        print(f"Execution Time: {execution_time:.2f} seconds")

        return jsonify({
            "execution_time": f"{execution_time:.2f} seconds",
            "result_count": len(results)  # Show how many rows were returned
        })

    except Exception as e:
        # Log the error in more detail
        print(f"Error occurred: {str(e)}")  # Print the exception message to the console
        return jsonify({"error": str(e)}), 500


#Fast query 
@app.route('/fast_query')
def fast_query():
    start_time = time.time()
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Only order in the CTE and join without an additional order
                cur.execute("""
                    SELECT 
                        c.name,
                        c.email,
                        f.name AS flower_name,
                        o.order_date AS order_date
                    FROM team9_orders o
                    JOIN team9_customers c ON o.customer_id = c.id
                    JOIN team9_flowers f ON o.flower_id = f.id
                    WHERE o.order_date >= CURRENT_DATE - INTERVAL '365 days'
                    LIMIT 100;
                """)
                
                _ = cur.fetchall()  # Execute query (no need to store results here)

        # Calculate execution time
        execution_time = time.time() - start_time  # Calculate execution time
        print(f"Execution Time: {execution_time:.2f} seconds")  # Print execution time

        # Return the execution time
        return jsonify({
            "execution_time": f"{execution_time:.2f} seconds"
        })

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log error message
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)