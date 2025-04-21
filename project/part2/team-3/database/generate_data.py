import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta
from db_connection import get_db_connection
import time

# Secure encryption key for PostgreSQL pgp_sym_encrypt
# This key should be stored securely in production, not hardcoded
ENCRYPTION_KEY = "123"

def generate_customers(num_customers=100000):
    fake = Faker()
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return
    
    try:
        cur = conn.cursor()
        print("Clearing existing customer data...")
        
        # Create pgcrypto extension if it doesn't exist
        cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
        conn.commit()
        
        # Clear both customer tables
        cur.execute("TRUNCATE TABLE team3_customers CASCADE")
        cur.execute("TRUNCATE TABLE team3_customers_encrypted CASCADE")
        conn.commit()
        
        print(f"Generating {num_customers} customers...")
        
        # Generate customers in batches of 1000
        batch_size = 1000
        for i in range(0, num_customers, batch_size):
            current_batch = min(batch_size, num_customers - i)
            unencrypted_values = []
            encrypted_values = []
            
            for j in range(current_batch):
                customer_id = i + j  # Generate ID in Python
                name = fake.name()
                email = fake.email()
                
                # Prepare values for both tables using the same ID
                unencrypted_values.append(f"({customer_id}, '{name}', '{email}')")
                encrypted_values.append(f"({customer_id}, '{name}', pgp_sym_encrypt('{email}', '{ENCRYPTION_KEY}'))")
            
            # Insert into unencrypted table
            unencrypted_query = f"""
                INSERT INTO team3_customers (id, name, email)
                VALUES {','.join(unencrypted_values)}
            """
            cur.execute(unencrypted_query)
            
            # Insert into encrypted table
            encrypted_query = f"""
                INSERT INTO team3_customers_encrypted (id, name, email)
                VALUES {','.join(encrypted_values)}
            """
            cur.execute(encrypted_query)
            
            conn.commit()
            print(f"Inserted {i + current_batch} customers into both tables...")
            
            # Verify the current batch
            cur.execute("""
                SELECT COUNT(*) 
                FROM team3_customers c1
                JOIN team3_customers_encrypted c2 ON c1.id = c2.id
                WHERE c1.id >= %s AND c1.id < %s
                AND c1.name = c2.name 
                AND c1.email = pgp_sym_decrypt(c2.email::bytea, %s)::text
            """, (i, i + current_batch, ENCRYPTION_KEY))
            batch_matches = cur.fetchone()[0]
            
            if batch_matches != current_batch:
                print(f"ERROR: Batch verification failed! Only {batch_matches} out of {current_batch} records match.")
                print("Terminating script due to data integrity issues.")
                exit(1)
        
        print("Customer generation complete!")
        
        # Final verification of all data
        print("\nVerifying all customer data...")
        cur.execute("SELECT COUNT(*) FROM team3_customers")
        unencrypted_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM team3_customers_encrypted")
        encrypted_count = cur.fetchone()[0]
        
        cur.execute("""
            SELECT COUNT(*) 
            FROM team3_customers c1
            JOIN team3_customers_encrypted c2 ON c1.id = c2.id
            WHERE c1.name = c2.name 
            AND c1.email = pgp_sym_decrypt(c2.email::bytea, %s)::text
        """, (ENCRYPTION_KEY,))
        joined_count = cur.fetchone()[0]
        
        print(f"Unencrypted customers: {unencrypted_count}")
        print(f"Encrypted customers: {encrypted_count}")
        print(f"Joined matching records: {joined_count}")
        
        if unencrypted_count != encrypted_count or unencrypted_count != joined_count or joined_count != num_customers:
            print("ERROR: Final data verification failed! Counts do not match.")
            print(f"Expected {num_customers} records in all tables and matches.")
            print(f"Unencrypted table has {unencrypted_count} records")
            print(f"Encrypted table has {encrypted_count} records")
            print(f"Only {joined_count} records match between tables")
            print("Terminating script due to data integrity issues.")
            exit(1)
            
        print(f"All counts match: {unencrypted_count == encrypted_count == joined_count == num_customers}")
        
    except Exception as e:
        print(f"Error generating customers: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def generate_orders(num_orders=500000):
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return
    
    try:
        cur = conn.cursor()
        print("Clearing existing order data...")
        
        # Clear both order tables
        cur.execute("TRUNCATE TABLE team3_orders CASCADE")
        cur.execute("TRUNCATE TABLE team3_orders_encrypted CASCADE")
        conn.commit()
        
        print(f"Generating {num_orders} orders...")
        
        # Get customer IDs from unencrypted table (we'll use these for both tables)
        cur.execute("SELECT id FROM team3_customers")
        customer_ids = [row[0] for row in cur.fetchall()]
        
        # Get all flower IDs
        cur.execute("SELECT flower_id FROM team3_flowers")
        flower_ids = [row[0] for row in cur.fetchall()]
        
        if not customer_ids or not flower_ids:
            print("No customers or flowers found in database")
            return
        
        # Generate orders in batches of 1000
        batch_size = 1000
        for i in range(0, num_orders, batch_size):
            current_batch = min(batch_size, num_orders - i)
            unencrypted_values = []
            encrypted_values = []
            
            for j in range(current_batch):
                order_id = i + j  # Generate ID in Python
                # Get random IDs (using same customer_id for both tables)
                customer_id = random.choice(customer_ids)
                flower_id = random.choice(flower_ids)
                
                # Generate a random date within the last 5 years
                order_date = datetime.now() - timedelta(days=random.randint(0, 1825))
                date_str = order_date.date().isoformat()
                
                # Prepare values for both tables using the same ID
                unencrypted_values.append(f"({order_id}, {customer_id}, {flower_id}, '{date_str}')")
                encrypted_values.append(f"({order_id}, {customer_id}, {flower_id}, pgp_sym_encrypt('{date_str}', '{ENCRYPTION_KEY}'))")
            
            # Insert into unencrypted table
            unencrypted_query = f"""
                INSERT INTO team3_orders (id, customer_id, flower_id, order_date)
                VALUES {','.join(unencrypted_values)}
            """
            cur.execute(unencrypted_query)
            
            # Insert into encrypted table
            encrypted_query = f"""
                INSERT INTO team3_orders_encrypted (id, customer_id, flower_id, order_date)
                VALUES {','.join(encrypted_values)}
            """
            cur.execute(encrypted_query)
            
            conn.commit()
            print(f"Inserted {i + current_batch} orders into both tables...")
            
            # Verify the current batch has matching data between the encrypted and unencrypted tables
            cur.execute("""
                SELECT COUNT(*) 
                FROM team3_orders o1
                JOIN team3_orders_encrypted o2 ON o1.id = o2.id
                WHERE o1.id >= %s AND o1.id < %s
                AND o1.customer_id = o2.customer_id 
                AND o1.flower_id = o2.flower_id
                AND o1.order_date = pgp_sym_decrypt(o2.order_date::bytea, %s)::date
            """, (i, i + current_batch, ENCRYPTION_KEY))
            batch_matches = cur.fetchone()[0]
            
            if batch_matches != current_batch:
                print(f"ERROR: Batch verification failed! Only {batch_matches} out of {current_batch} records match.")
                print("Terminating script due to data integrity issues.")
                exit(1)
        
        print("Order generation complete!")
        
        # Final verification of all data
        print("\nVerifying all order data...")
        cur.execute("SELECT COUNT(*) FROM team3_orders")
        unencrypted_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM team3_orders_encrypted")
        encrypted_count = cur.fetchone()[0]
        
        cur.execute("""
            SELECT COUNT(*) 
            FROM team3_orders o1
            JOIN team3_orders_encrypted o2 ON o1.id = o2.id
            WHERE o1.customer_id = o2.customer_id 
            AND o1.flower_id = o2.flower_id
            AND o1.order_date = pgp_sym_decrypt(o2.order_date::bytea, %s)::date
        """, (ENCRYPTION_KEY,))
        joined_count = cur.fetchone()[0]
        
        print(f"Unencrypted orders: {unencrypted_count}")
        print(f"Encrypted orders: {encrypted_count}")
        print(f"Joined matching records: {joined_count}")
        
        if unencrypted_count != encrypted_count or unencrypted_count != joined_count or joined_count != num_orders:
            print("ERROR: Final data verification failed! Counts do not match.")
            print(f"Expected {num_orders} records in all tables and matches.")
            print(f"Unencrypted table has {unencrypted_count} records")
            print(f"Encrypted table has {encrypted_count} records")
            print(f"Only {joined_count} records match between tables")
            print("Terminating script due to data integrity issues.")
            exit(1)
            
        print(f"All counts match: {unencrypted_count == encrypted_count == joined_count == num_orders}")
        
    except Exception as e:
        print(f"Error generating orders: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    start_time = time.time()
    
    # First ensure we have some flowers in the database
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM team3_flowers")
        flower_count = cur.fetchone()[0]
        if flower_count == 0:
            print("No flowers found in database. Please ensure you have some flowers before running this script.")
            exit(1)
        cur.close()
        conn.close()
    
    # Uncomment the functions below if you want to regenerate the customers and orders table entries
    # generate_customers()
    # generate_orders()
    
    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds") 