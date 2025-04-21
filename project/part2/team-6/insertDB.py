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
    # cur.execute("""
    #     CREATE TABLE team6_flowers (
    #         id SERIAL PRIMARY KEY,
    #         name VARCHAR(100) NOT NULL,
    #         last_watered DATE NOT NULL,
    #         water_level INT NOT NULL,
    #         min_water_required INT NOT NULL
    #         );
    # """)

    # print("Tables created successfully.")

    # --- INSERT DATA ---
    cur.execute("INSERT INTO team6_flowers (name, last_watered, water_level, min_water_required) VALUES ('Rose', '2025-02-27', 10, 100) RETURNING id;")
    rose_id = cur.fetchone()[0]

    #
    # cur.execute("INSERT INTO flowers (name, color, price, stock) VALUES ('Tulip', 'Yellow', 3.50, 80) RETURNING flower_id;")
    # tulip_id = cur.fetchone()[0]

    # cur.execute("INSERT INTO customers (name, email, phone, address) VALUES ('Alice Johnson', 'alice@example.com', '123-456-7890', '123 Garden St') RETURNING customer_id;")
    # alice_id = cur.fetchone()[0]

    # print("Inserted sample data.")

    # # --- CREATE AN ORDER ---
    # cur.execute(f"INSERT INTO orders (customer_id, total) VALUES ({alice_id}, 0) RETURNING order_id;")
    # order_id = cur.fetchone()[0]

    # cur.execute(f"INSERT INTO order_details (order_id, flower_id, quantity, price) VALUES ({order_id}, {rose_id}, 3, 5.99);")
    # cur.execute(f"INSERT INTO order_details (order_id, flower_id, quantity, price) VALUES ({order_id}, {tulip_id}, 2, 3.50);")

    # # --- UPDATE STOCK ---
    # cur.execute(f"UPDATE flowers SET stock = stock - 3 WHERE flower_id = {rose_id};")
    # cur.execute(f"UPDATE flowers SET stock = stock - 2 WHERE flower_id = {tulip_id};")

    # # --- UPDATE ORDER TOTAL ---
    # cur.execute(f"""
    #     UPDATE orders
    #     SET total = (SELECT SUM(quantity * price) FROM order_details WHERE order_id = {order_id})
    #     WHERE order_id = {order_id};
    # """)

    # print("Order placed successfully.")

    # # --- DELETE AN ORDER (Example) ---
    # cur.execute(f"DELETE FROM orders WHERE order_id = {order_id};")
    # print("Deleted an order.")

    # Close cursor and connection
    cur.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("Error:", e)