from dotenv import load_dotenv, dotenv_values
import psycopg2, sys, os

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# import postgress-crud.py into app.py
import postgress_crud as db

'''
# Input the absolute path to the .env file
load_dotenv()

# AWS PostgreSQL connection
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_URI')}:5432/{os.getenv('DB_NAME')}"
'''
try:
    conn = db.get_db_connection()
    print("Connected to PostgreSQL successfully!")
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print("PostgreSQL Version:", db_version)
    cur.close()
    conn.close()
    print("Connection closed.")
    
    '''
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
    '''

except Exception as e:
    print("Error connecting to PostgreSQL:", e)