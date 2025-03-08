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
    cur.execute("""
    INSERT INTO team5_flowers (name, last_watered, water_level, min_water_required)
    VALUES
    ('Rose', '2024-02-10', 20, 5),
    ('Tulip', '2024-02-08', 10, 7),
    ('Lily', '2024-02-05', 3, 5),
    ('Sunflower', '2024-02-07', 5, 3),
    ('Daisy', '2024-02-06', 7, 4),
    ('Orchid', '2024-02-09', 15, 10),
    ('Daffodil', '2024-02-04', 2, 5),
    ('Poppy', '2024-02-03', 1, 5),
    ('Carnation', '2024-02-02', 0, 5),
    ('Hyacinth', '2024-02-01', 0, 5);
    ('Lavender', '2024-02-01', 0, 5);
    ('Peony', '2024-02-01', 0, 5);
    """)

    print("Inserted data to successfully!")


    # Close cursor and connection
    cur.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("Error:", e)