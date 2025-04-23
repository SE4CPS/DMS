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

    cur.execute("""
    INSERT INTO team5_flowers (name, last_watered, water_level, min_water_required)
    VALUES
    ('Rose', '2025-04-10', 20, 5),
    ('Tulip', '2025-04-08', 10, 7),
    ('Lily', '2025-04-05', 3, 5),
    ('Sunflower', '2025-04-07', 5, 3),
    ('Daisy', '2025-04-06', 7, 4),
    ('Orchid', '2025-04-09', 15, 10),
    ('Daffodil', '2025-04-04', 2, 5),
    ('Poppy', '2025-04-03', 1, 5),
    ('Carnation', '2025-04-02', 0, 5),
    ('Hyacinth', '2025-04-01', 0, 5),
    ('Lavender', '2025-04-01', 0, 5),
    ('Peony', '2025-04-01', 0, 5);
    """)

    # for i in range(42191,100000):
    #     customer = i %42190 + 1
    #     flower = i % 10 + 1
    #     date =f"2025-03-{i % 31 + 1:02d}"
    #     cur.execute("""
    #     INSERT INTO team5_orders (customer_id,flower_id, order_date)
    #     VALUES (%s, %s, %s)
    #     """,(customer,flower,date))
    #     print(f"Inserted order {i}")

    print("Inserted data to successfully!")


    # Close cursor and connection
    cur.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("Error:", e)