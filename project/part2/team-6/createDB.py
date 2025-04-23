from unittest import result
import psycopg2
import random
import time
# ----------- update this file ------------------
# import Faker - a library to get fake but realistic names and emails
from faker import Faker

# initialize Faker
fake = Faker()
# ------------------------------------------------

# Neon PostgreSQL connection details
# DATABASE_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"
# we're now using Render, which expires on May 22nd
DATABASE_URL = "postgresql://team6_user:cWWhj2yh0jbqcsRHxQhCzbgRi8k6f4aw@dpg-d041caadbo4c73ca3tgg-a.oregon-postgres.render.com/team6"

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True  # Enable auto-commit for transactions
    print("Connected to PostgreSQL successfully!")

    # Create a cursor object
    cur = conn.cursor()
    # cur.execute("""
    #     DROP TABLE team6_flowers;
    # """)
    # --- CREATE TABLES ---
    # cur.execute("""
    #     CREATE TABLE team6_flowers (
    #         id SERIAL PRIMARY KEY,
    #         name VARCHAR(100) NOT NULL,
    #         last_watered DATE NOT NULL,
    #         water_level INT NOT NULL CHECK(water_level >= 0),
    #         min_water_required INT NOT NULL
    #         );
    # """)

    # cur.execute("""
    #     CREATE TABLE team6_customers (
    #         id SERIAL PRIMARY KEY,
    #         name VARCHAR(100),
    #         email VARCHAR(100)
    #     );
    # """)

    # ----- make a second version of the customers table with encryptions -------------------------------
    # cur.execute("""
    #     CREATE TABLE team6_customers_secure (
    #         id SERIAL PRIMARY KEY,
    #         name TEXT,
    #         email BYTEA -- encrypted data is stored as bytea
    #     );
    # """)
    # ---------------------------------------------------------------------------------------------------
    
    # ------------------- inserting rows to the encrypted table -----------------------------------------
    # BATCH_SIZE = 1000
    # TOTAL_RECORDS = 100_000
    # ENCRYPTION_KEY = "secret_key"
    
    # conn = psycopg2.connect(DATABASE_URL)
    # conn.autocommit = True
    # cur = conn.cursor()

    # for i in range(0, TOTAL_RECORDS, BATCH_SIZE):
    #     rows = [
    #         (
    #             fake.name(),
    #             fake.name() + "@gmail.com" # we're using fake.name() + "@gmail.com" instead of fake.email() to have emails that end with @gmail.com
    #         )
    #         for _ in range(BATCH_SIZE)
    #     ]

    #     values_sql = ",".join(
    #         cur.mogrify("(%s, pgp_sym_encrypt(%s, %s))", (name, email, ENCRYPTION_KEY)).decode("utf-8")
    #         for name, email in rows
    #     )

    #     cur.execute(
    #         "INSERT INTO team6_customers_secure (name, email) VALUES " + values_sql
    #     )
    #     print(f"Inserted {i + BATCH_SIZE} / {TOTAL_RECORDS} customers")

    # print("Insertion complete.")
    # -----------------------------------------------------------------------------------------------

    # ------------------------ testing out by selecting 1 value of the encrypted table --------------
    # cur.execute("""
    #     SELECT 
    #         id, 
    #         name, 
    #         pgp_sym_decrypt(email, 'secret_key') AS email
    #     FROM team6_customers_secure
    #     WHERE id=1;
    # """)
    # row = cur.fetchone()
    # if row:
    #     print("Customer Record:", row)
    # else:
    #     print("No record found with id=1")
    # -------------------------------------------------------------------------------------------------

    # cur.execute("""
    #     CREATE TABLE team6_orders (
    #         id SERIAL PRIMARY KEY,
    #         customer_id INT REFERENCES team6_customers(id),
    #         flower_id INT REFERENCES team6_flowers(id),
    #         order_date DATE
    #     );
    # """)

    # ------------ generate fake names and emails for the new tables -------------------------------
    # customers = [(fake.name(), fake.email()) for _ in range(100000)]
    # args_str = ",".join(cur.mogrify("(%s, %s)", customer).decode('utf-8') for customer in customers)
    # ------------ add records into the customer table ---------------------------------------------
    # instead of: cur.execute(f"INSERT INTO team6_customers (name, email) VALUES {args_str}")
    # BATCH_SIZE = 5000
    # for i in range(0, len(customers), BATCH_SIZE):
    #     batch = customers[i:i + BATCH_SIZE]
    #     args_str = ",".join(cur.mogrify("(%s, %s)", customer).decode('utf-8') for customer in batch)
    #     cur.execute(f"INSERT INTO team6_customers (name, email) VALUES {args_str}")
    #     print(f"Inserted {i + BATCH_SIZE} / {len(customers)} customers")

    # print("Inserted 100,000 customers successfully.")
    # cur.execute("SELECT * FROM team6_customers WHERE id=1;")
    # row = cur.fetchone()
    # if row:
    #     print("Customer Record:", row)
    # else:
    #     print("No record found with id=1")
    
    # ----------- inserting orders ---------------
    # Fetch existing customer IDs
    # cur.execute("SELECT id FROM team6_customers")
    # customer_ids = [row[0] for row in cur.fetchall()]

    # Fetch existing flower IDs
    # cur.execute("SELECT id FROM team6_flowers")
    # flower_ids = [row[0] for row in cur.fetchall()]

    # if not customer_ids or not flower_ids:
    #     raise Exception("No customers or flowers found in the database.")

    # Generate 250,000 random orders
    # orders = [
    #     (random.choice(customer_ids), random.choice(flower_ids), fake.date_between(start_date="-1y", end_date="today"))
    #     for _ in range(250000)
    # ]

    # Batch insert for efficiency
    # args_str = ",".join(cur.mogrify("(%s, %s, %s)", order).decode('utf-8') for order in orders)
    # instead of: cur.execute(f"INSERT INTO team6_orders (customer_id, flower_id, order_date) VALUES {args_str}")
    # BATCH_SIZE = 5000
    # for i in range(0, len(orders), BATCH_SIZE):
    #     batch = orders[i:i + BATCH_SIZE]
    #     args_str = ",".join(cur.mogrify("(%s, %s, %s)", order).decode('utf-8') for order in batch)
    #     cur.execute(f"INSERT INTO team6_orders (customer_id, flower_id, order_date) VALUES {args_str}")
    #     print(f"Inserted {i + BATCH_SIZE} / {len(orders)} orders")


    # print("Inserted 250,000 orders successfully.")

    # cur.execute("SELECT * FROM team6_orders WHERE id=1;")
    # row = cur.fetchone()
    # if row:
    #     print("Customer Record:", row)
    # else:
    #     print("No record found with id=1")

    # # ----- start timer for JOIN operation -----------
    # start_time = time.time()

    # cur.execute("""
    #     SELECT name
    #     FROM team6_customers;
    # """)

    # # ----- end timer for JOIN operation -----------
    # end_time = time.time()
    # # ------ calculate run time ---------------
    # elapsed_time = end_time - start_time
    # print(f"Query executed in: {elapsed_time:.4f} seconds")
    # print("Tables created successfully.")

    # ---------------------------------------------------------

    # #--------------- query with LIKE operator (runtime = ~0.4 sec with LIMIT = 5000, ~ 4 sec without limits) -----------------------
    # # SELECT * FROM team6_customers
    # #     WHERE email LIKE '%@%'
    # #     LIMIT 5000;
    
    # ----- start timer for INNER JOIN query -----------
    # start_time = time.time()

    # cur.execute("""
    #     SELECT 
    #         c.id AS customer_id,
    #         c.name AS customer_name,
    #         c.email,
    #         f.id AS flower_id,
    #         f.name AS flower_name,
    #         o.order_date
    #     FROM team6_orders o
    #     INNER JOIN team6_customers c ON o.customer_id = c.id
    #     INNER JOIN team6_flowers f ON o.flower_id = f.id;        
    # """)

    # # ----- end timer for INNER JOIN operation -----------
    # end_time = time.time()
    # # ------ calculate run time ---------------
    # elapsed_time = end_time - start_time
    # result = cur.fetchone()
    # print("query result", result)
    # print(f"Query executed in: {elapsed_time:.4f} seconds")

    # ----------- start timer for SELECT query of the encrypted table (run time ~ 25 sec) --------------------
    # start_time = time.time()

    # cur.execute("""
    #     SELECT 
    #         id, 
    #         name, 
    #         pgp_sym_decrypt(email, 'secret_key') AS email
    #     FROM team6_customers_secure
    # """)
    
    # just to test the query - put LIMIT 1 (or WHERE id=1) to test it out
    # row = cur.fetchone()
    # if row:
    #     print("Customer Record:", row)
    # else:
    #     print("No record found with id=1")

    # ------------- end timer for SELECT query of the encrypted table ---------------------
    # end_time = time.time()
    # --------------- calculate run time - took about 25 seconds first try --------------------------------------------------
    # elapsed_time = end_time - start_time
    # print(f"Query executed in: {elapsed_time:.4f} seconds")
    
    # -------------------------------------------------------------
    # --- INSERT DATA ---
    #cur.execute("INSERT INTO team6_flowers (name, last_watered, water_level, min_water_required) VALUES ('Rose', '2025-02-27', 10, 100) RETURNING id;")
    #rose_id = cur.fetchone()[0]

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