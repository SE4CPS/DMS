import psycopg2

DATABASE_URL = ""

# Bikes to insert
bikes_to_insert = [
    ('Mountain Bike', 500.00),
    ('Road Bike', 700.00),
    ('Hybrid Bike', 300.00),
    ('Electric Bike', 2500.00),
    ('Kids Bike', 150.00)
]

insert_command = """
INSERT INTO bike (bike_model, bike_price) VALUES (%s, %s)
"""

try:
    # Connect to the database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Insert bikes into the table
    cur.executemany(insert_command, bikes_to_insert)
    
    # Commit the changes
    conn.commit()
    
    print("5 bikes inserted successfully.")
    
except psycopg2.DatabaseError as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure that the database connection is closed
    if conn is not None:
        cur.close()
        conn.close()
