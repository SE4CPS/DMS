# Run this code using python3 -m backend.test_queries 
# This is so that Python can treat the script as a module within a package structure. It will include the parent directory to the Python path as well.


from database.db_connection import get_db_connection

def test_select_tables():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()

        # Test query to show all tables
        print("\n=== Checking existing tables ===")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'team3_%'
        """)
        tables = cur.fetchall()
        print("Found tables:", [table[0] for table in tables])

        select_all_tables(cur)

        cur.close()
        conn.close()
        
def test_insert_tables():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        
        # Test query to show all tables
        print("\n=== Checking existing tables ===")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'team3_%'
        """)
        tables = cur.fetchall()
        print("Found tables:", [table[0] for table in tables])
        
        # Test inserting sample data
        print("\n=== Inserting sample data ===")
        try:
            # Insert a customer
            cur.execute("""
                INSERT INTO team3_customers (name, email)
                VALUES ('Test Customer', 'test@example.com')
                RETURNING id
            """)
            customer_id = cur.fetchone()[0]
            print(f"Inserted customer with ID: {customer_id}")
            
            # Insert a flower
            cur.execute("""
                INSERT INTO team3_flowers (flower_name, last_watered, water_level, min_water_required)
                VALUES ('Test Flower', CURRENT_DATE, 100, 50)
                RETURNING flower_id
            """)
            flower_id = cur.fetchone()[0]
            print(f"Inserted flower with ID: {flower_id}")
            
            # Insert an order
            cur.execute("""
                INSERT INTO team3_orders (customer_id, flower_id, order_date)
                VALUES (%s, %s, CURRENT_DATE)
                RETURNING id
            """, (customer_id, flower_id))
            order_id = cur.fetchone()[0]
            print(f"Inserted order with ID: {order_id}")
            
            # View all data
            select_all_tables(cur)
            
            conn.commit()
            
        except Exception as e:
            print("Error during testing:", e)
            conn.rollback()
            
        finally:
            cur.close()
            conn.close()

def select_all_tables(cur):
    print("\n=== Viewing all data ===")
            
    print("\nCustomers Execution Time:")
    cur.execute("EXPLAIN ANALYZE SELECT * FROM team3_customers")
    for row in cur.fetchall():
        print(row)

    print("\nCustomers Data:")
    cur.execute("SELECT * FROM team3_customers")
    for row in cur.fetchall():
        print(row)
                

    print("\nFlowers Execution Time:")
    cur.execute("EXPLAIN ANALYZE SELECT * FROM team3_flowers")
    for row in cur.fetchall():
        print(row)

    print("\nFlowers:")
    cur.execute("SELECT * FROM team3_flowers")
    for row in cur.fetchall():
        print(row)
                
    print("\nOrders Execution Time:")
    cur.execute("EXPLAIN ANALYZE SELECT * FROM team3_orders")
    for row in cur.fetchall():
        print(row)
    print("\nOrders:")
    cur.execute("SELECT * FROM team3_orders")
    for row in cur.fetchall():
        print(row)

if __name__ == "__main__":
    test_select_tables() 
