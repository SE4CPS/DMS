import psycopg2

DATABASE_URL = ""

drop_table_command = """
DROP TABLE IF EXISTS bike
"""

try:
    # Connect to the database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Drop the bikes table
    cur.execute(drop_table_command)
    
    # Commit the changes
    conn.commit()
    
    print("Bikes table dropped successfully.")
    
except psycopg2.DatabaseError as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure that the database connection is closed
    if conn is not None:
        cur.close()
        conn.close()