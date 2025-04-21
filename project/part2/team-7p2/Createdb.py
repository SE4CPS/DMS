import psycopg2
import random
from datetime import datetime, timedelta

# Database connection details
DATABASE_URL = "postgresql://neondb_owner:npg_QuIm1wktTiV0@ep-nameless-base-aab6w7ti-pooler.westus3.azure.neon.tech/neondb?sslmode=require"

def get_db_connection():
    """Creates and returns a new database connection."""
    return psycopg2.connect(DATABASE_URL)

def populate_data():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Ensure the pgcrypto extension is available
        cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

        print("Inserting encrypted customers:")
        for i in range(10000000):  # Consider reducing this number for testing purposes
            name = f'Customer {i}'
            email = f'customer{i}@example.com'
            cur.execute("""
                INSERT INTO team7p2_customers (name, email)
                VALUES (
                    pgp_sym_encrypt(%s, 'secret_key'),
                    pgp_sym_encrypt(%s, 'secret_key')
                );
            """, (name, email))
            if i < 5:  # Only print the first few to avoid clutter
                print(f"Inserted customer {i}: {name}, {email}")

        print("\nInserting random orders:")
        for i in range(10000000):  # Again, consider reducing the number
            customer_id = random.randint(1, 10)
            flower_id = random.randint(1, 3)  # Ensure you have at least 5 flowers
            order_date = datetime.today() - timedelta(days=random.randint(0, 365))
            cur.execute("""
                INSERT INTO team7p2_orders (customer_id, flower_id, order_date)
                VALUES (%s, %s, %s);
            """, (customer_id, flower_id, order_date))
            if i < 5:  # Only print the first few to avoid too much output
                print(f"Inserted order {i}: Customer ID {customer_id}, Flower ID {flower_id}, Date {order_date}")

        conn.commit()
        print("Inserted 10000000 encrypted customers and 10000000 orders successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    populate_data()