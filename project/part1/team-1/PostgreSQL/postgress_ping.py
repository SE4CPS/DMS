import psycopg2

# AWS PostgreSQL connection
DATABASE_URL = ""

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    print("Connected to PostgreSQL successfully!")

    # Create a cursor object
    cur = conn.cursor()

    # Execute a simple query
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print("PostgreSQL Version:", db_version)

    # Close cursor and connection
    cur.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("Error connecting to PostgreSQL:", e)