from dotenv import load_dotenv, dotenv_values
import psycopg2
import os

# Input the absolute path to the .env file
load_dotenv()

# AWS PostgreSQL connection
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_URI')}:5432/{os.getenv('DB_NAME')}"

# change flowerTest to team1_flowers after testing is sucessful
try:
    # Connect to PostgreSQL database
    def get_db_connection():
        return psycopg2.connect(DATABASE_URL)
    
    '''
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True  # Enable auto-commit for transactions
    print("Connected to PostgreSQL successfully!")
    '''
    # Create a cursor object
    conn = get_db_connection()
    cur = conn.cursor()


    # --- CREATING TABLE ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS flowerTest (
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

   # print("Table created successfully.")

    # --- INSERT DATA ---
    # -- into team1_flowers table
    cur.execute("INSERT INTO flowerTest (name, environment, initial_water_level_in_inches,  current_water_level_in_inches, minimum_water_level_in_inches, last_watered) VALUES ('Rose','outdoor',20, 15, 12, '2025-02-28') RETURNING flower_id;")
    rose_id = cur.fetchone()[0]

    cur.execute("INSERT INTO flowerTest (name, environment, initial_water_level_in_inches,  current_water_level_in_inches, minimum_water_level_in_inches, last_watered) VALUES ('Marigold','indoor', 18, 10, 16, '2025-02-26') RETURNING flower_id;")
    marigold_id = cur.fetchone()[0]

    cur.execute("INSERT INTO flowerTest (name, environment, initial_water_level_in_inches,  current_water_level_in_inches, minimum_water_level_in_inches, last_watered) VALUES ('Jasmine','indoor',23, 14, 15, '2025-03-01')  RETURNING flower_id;")
    jasmine_id = cur.fetchone()[0]
   
    cur.execute("INSERT INTO flowerTest (name, environment, initial_water_level_in_inches,  current_water_level_in_inches, minimum_water_level_in_inches, last_watered) VALUES ('Sunflower','outdoor',19, 16, 13, '2025-02-25')  RETURNING flower_id;")
    sunflower_id = cur.fetchone()[0]

    cur.execute("INSERT INTO flowerTest (name, environment, initial_water_level_in_inches,  current_water_level_in_inches, minimum_water_level_in_inches, last_watered) VALUES ('Tulip','outdoor',24, 20, 18, '2025-03-02')  RETURNING flower_id;")
    tulip_id = cur.fetchone()[0]
    

    print("Inserted sample data.")

    
    # Close cursor and connection
    cur.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("Error:", e)