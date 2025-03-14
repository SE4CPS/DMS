import psycopg2

# Neon PostgreSQL connection details
DATABASE_URL = "postgresql://flower_db_owner:npg_51HLIvYdpuVQ@ep-green-block-a8ifhr0o-pooler.eastus2.azure.neon.tech/flower_db?sslmode=require"

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True  # Enable auto-commit for transactions
    print("Connected to PostgreSQL successfully!")

    # Create a cursor object
    cur = conn.cursor()

    # --- CREATE TABLES ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS team9_flowers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            last_watered DATE NOT NULL,
            water_level INT NOT NULL,
            min_water_required INT NOT NULL
        );
    """)

    print("Tables created successfully.")

    # --- INSERT DATA --- 
    
    # Insert data using this format:
        # "INSERT INTO team9_flowers (name, last_watered, water_level, min_water_required) VALUES (string, string, int, int) RETURNING id"
    
    cur.execute("INSERT INTO team9_flowers( name, last_watered, water_level, min_water_required) VALUES ('Rose', '2024-02-10', 20, 5) RETURNING id")
    rose_id = cur.fetchone()[0]

    cur.execute("INSERT INTO team9_flowers( name, last_watered, water_level, min_water_required) VALUES ('Tulip', '2024-02-08', 10, 7) RETURNING id")
    tulip_id = cur.fetchone()[0]

    cur.execute("INSERT INTO team9_flowers( name, last_watered, water_level, min_water_required) VALUES ('Lily', '2024-02-05', 3, 5) RETURNING id")
    lily_id = cur.fetchone()[0]

    print("Inserted sample data.")

    # Close cursor and connection
    cur.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("Error:", e)