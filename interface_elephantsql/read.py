import psycopg2

DATABASE_URL = ""

# SQL command to query all entries from the "bikes" table
query_command = "SELECT bike_id, bike_model, bike_price FROM bike"

try:
    # Connect to the database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Execute the query
    cur.execute(query_command)
    
    # Fetch all rows from the table
    rows = cur.fetchall()
    
    # Print the rows
    for row in rows:
        print(f"Bike ID: {row[0]}, Model: {row[1]}, Price: ${row[2]}")
    
except psycopg2.DatabaseError as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure that the database connection is closed
    if conn is not None:
        cur.close()
        conn.close()
