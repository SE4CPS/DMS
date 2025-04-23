import psycopg2

# Neon PostgreSQL connection details
DATABASE_URL = "postgresql://neondb_owner:npg_tRjAlmCi4y6n@ep-bold-lake-a5wpofnx-pooler.us-east-2.aws.neon.tech/dbms?sslmode=require"

try:
   # Connect to PostgreSQL
   conn = psycopg2.connect(DATABASE_URL)
   conn.autocommit = True  # Enable auto-commit for transactions
   print("Connected to PostgreSQL successfully!")

   # Create a cursor object
   cur = conn.cursor()

   # --- CREATE TABLES ---
   cur.execute("""
   CREATE TABLE IF NOT EXISTS team5_flowers (
   id SERIAL PRIMARY KEY,
   name VARCHAR(100) NOT NULL,
   last_watered DATE NOT NULL,
   water_level INT NOT NULL,
   min_water_required INT NOT NULL
   );
   """)

   cur.execute("""
   CREATE TABLE IF NOT EXISTS team5_customers(
   id SERIAL PRIMARY KEY,
   name varchar(100),
   email varchar(100)
   );
   """)

   cur.execute("""
   CREATE TABLE IF NOT EXISTS team5_orders(
   id SERIAL PRIMARY KEY,
   customer_id INT REFERENCES team5_customers(id),
   flower_id INT REFERENCES team5_flowers(id),
   order_date DATE
   );
   """)

   print("Tables created successfully.")

   # Close cursor and connection
   cur.close()
   conn.close()
   print("Connection closed.")

except Exception as e:
   print("Error:", e)
