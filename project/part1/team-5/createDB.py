
import psycopg2

# Neon PostgreSQL connection details
DATABASE_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True  # Enable auto-commit for transactions
    print("Connected to PostgreSQL successfully!")

    # Create a cursor object
    cur = conn.cursor()

    # --- CREATE TABLES ---
    cur.execute("""
 CREATE TABLE team5_flowers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    last_watered DATE NOT NULL,
    water_level INT NOT NULL,
    min_water_required INT NOT NULL
    );
 """)

    print("Tables created successfully.")

    # Close cursor and connection
    cur.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("Error:", e)