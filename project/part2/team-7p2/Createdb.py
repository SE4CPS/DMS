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
        # Ensure pgcrypto extension is available
        cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

        print("Inserting encrypted customers:")
        for i in range(10000):
            name = f'Customer {i}'
            email = f'customer{i}@example.com'
            cur.execute("""
                INSERT INTO team7_p2_customers (name, email)
                VALUES (
                    pgp_sym_encrypt(%s, 'secret_key'),
                    pgp_sym_encrypt(%s, 'secret_key')
                );
            """, (name, email))
            print(f"Inserted customer {i}: {name}, {email}")  # Prints every customer

        print("\nInserting random orders:")
        for i in range(10000):
            customer_id = random.randint(1, 10)
            flower_id = random.randint(1, 3)  # Ensure you have at least 3 flowers
            order_date = datetime.today() - timedelta(days=random.randint(0, 365))
            cur.execute("""
                INSERT INTO team7_p2_orders (customer_id, flower_id, order_date)
                VALUES (%s, %s, %s);
            """, (customer_id, flower_id, order_date))
            print(f"Inserted order {i}: Customer ID {customer_id}, Flower ID {flower_id}, Date {order_date}")  # Prints every order

        conn.commit()
        print("\nData insertion complete!")
    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
    finally:
        cur.close()
        conn.close()

# Call the function to populate the data
if __name__ == "__main__":
    populate_data()