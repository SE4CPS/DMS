# Import postgress_crud.py into postgress_ping.py to verify connection to the PostgreSQL database
import postgress_crud as db

try:
    # get_db_connection() is a function from postgress_crud.py
    conn = db.get_db_connection()
    print("Connected to PostgreSQL successfully!")
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print("PostgreSQL Version:", db_version)
    
    # Close cursor and connection
    cur.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("Error connecting to PostgreSQL:", e)