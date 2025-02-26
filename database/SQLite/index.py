import sqlite3
import random
import time
from datetime import datetime, timedelta

# Database setup
DB_FILE = "orders.db"

# Function to drop and recreate the table
def reset_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS orders;")  # Drop the table to reset data
    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,
            status TEXT
        );
    """)
    conn.commit()
    conn.close()
    print("Table reset complete!")

# Function to insert 100M rows in batches
def insert_data(batch_size=100000, total_rows=10000000):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    statuses = ["shipped", "pending", "canceled"]
    start_date = datetime(2020, 1, 1)

    print(f"Inserting {total_rows} rows in batches of {batch_size}...")

    for i in range(0, total_rows, batch_size):
        rows = [
            (
                random.randint(1, 1000000),  # customer_id
                (start_date + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),  # order_date
                random.choice(statuses)  # status
            )
            for _ in range(batch_size)
        ]
        cursor.executemany("INSERT INTO orders (customer_id, order_date, status) VALUES (?, ?, ?)", rows)
        conn.commit()
        print(f"Inserted {i + batch_size} rows...")

    conn.close()
    print("Data insertion complete!")

# Function to execute a query and measure execution time
def execute_query(query, desc):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    print(f"\nExecuting: {desc}")
    start_time = time.time()
    cursor.execute(query)
    conn.commit()
    elapsed = time.time() - start_time
    print(f"Time taken: {elapsed:.2f} seconds")
    conn.close()

# Main function
def main():
    # reset_table()  # Drop and recreate the table
    # insert_data()

    # Query without index
    execute_query("""
        EXPLAIN QUERY PLAN
        SELECT customer_id, COUNT(*) 
        FROM orders 
        WHERE customer_id BETWEEN 500000 AND 500500
          AND status IN ('shipped', 'pending')
          AND order_date BETWEEN '2023-01-01' AND '2023-12-31'
        GROUP BY customer_id
        ORDER BY order_date DESC, customer_id ASC;
    """, "Query WITHOUT Index")

    # Create index
    execute_query("CREATE INDEX IF NOT EXISTS idx_customer_date ON orders(customer_id, order_date);", "Creating Index")

    # Query with index
    execute_query("""
        EXPLAIN QUERY PLAN
        SELECT customer_id, COUNT(*) 
        FROM orders 
        WHERE customer_id BETWEEN 500000 AND 500500
          AND status IN ('shipped', 'pending')
          AND order_date BETWEEN '2023-01-01' AND '2023-12-31'
        GROUP BY customer_id
        ORDER BY order_date DESC, customer_id ASC;
    """, "Query WITH Index")

if __name__ == "__main__":
    main()
