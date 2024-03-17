import psycopg2

DATABASE_URL = ""

try:
    # Connect to your elephant SQL database
    conn = psycopg2.connect(DATABASE_URL)

    # Create a cursor object
    cur = conn.cursor()
    
    # Execute a query
    cur.execute("SELECT version();")

    # Fetch and print the result
    version = cur.fetchone()
    print(version)

    # Close the cursor and connection
    cur.close()
    conn.close()
    
except psycopg2.DatabaseError as error:
    print(f"Error: {error}")