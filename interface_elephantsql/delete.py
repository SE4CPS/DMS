import psycopg2

DATABASE_URL = ""

delete_command = """
DELETE FROM bike
"""

try:
    # Connect to the database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Delete all bikes from the table
    cur.execute(delete_command)
    
    # Commit the changes
    conn.commit()
    
    print("All bikes deleted successfully.")
    
except psycopg2.DatabaseError as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure that the database connection is closed
    if conn is not None:
        cur.close()
        conn.close()
