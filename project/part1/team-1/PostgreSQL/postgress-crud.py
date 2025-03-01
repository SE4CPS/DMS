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


    # --- CREATING TABLE ---

    cur.execute("""
        CREATE TABLE IF NOT EXISTS team1_flowers (
            flower_id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            environment TEXT NOT NULL DEFAULT 'outdoor' CHECK (environment = 'indoor' OR environment = 'outdoor'),
            initial_water_level_in_inches INTEGER NOT NULL DEFAULT 20,
            current_water_level_in_inches INTEGER NOT NULL CHECK (current_water_level_in_inches >= 0),
            minimum_water_level_in_inches INTEGER NOT NULL CHECK (minimum_water_level_in_inches >= 0),
            last_watered DATE,
            needs_water BOOL GENERATED ALWAYS AS (current_water_level_in_inches < minimum_water_level_in_inches) STORED
        );
    """)

    print("Table created successfully.")

    # --- INSERT DATA ---
    # -- into team1_flowers table
    #cur.execute("INSERT INTO team1_flowers (name, initial_water_level,  current_water_level, min_water_level, last_watered) VALUES ('Rose',10, 15, 12, '2024-02-34');")
    # water level was intially 10, it's current water level is 15, and the min water level is 12 (last watered was feb 24)
    #cur.fetchone()[0]

   # print("Inserted sample data.")

    
    # Close cursor and connection
    cur.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("Error:", e)