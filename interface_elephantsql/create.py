import psycopg2
from psycopg2 import sql

# Database connection string
DATABASE_URL = ""

# SQL command to create the "bike" table
create_table_command = sql.SQL("""
CREATE TABLE IF NOT EXISTS bike (
    bike_id SERIAL PRIMARY KEY,
    bike_model VARCHAR(255) NOT NULL,
    bike_price DECIMAL(10, 2)
)
""")

try:
    # Connect to the database using the DATABASE_URL
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Execute the create table command
    cur.execute(create_table_command)
    
    # Commit the changes
    conn.commit()
    
    print("Table 'bikes' created successfully.")
    
except psycopg2.DatabaseError as e:
    print(f"An error occurred: {e}")
finally:
    # Close communication with the database
    if cur: cur.close()
    if conn: conn.close()