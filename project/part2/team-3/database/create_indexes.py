from database.db_connection import get_db_connection

def create_indexes():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            # Create index on customer_id in orders table for faster joins
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_orders_customer_id 
                ON team3_orders(customer_id);
            """)
            
            # Create index on email in customers table for faster filtering
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_customers_email 
                ON team3_customers(email);
            """)
            
            # Create index on order_date in orders table for faster sorting
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_orders_order_date 
                ON team3_orders(order_date DESC);
            """)
            
            conn.commit()
            print("Indexes created successfully!")
            
        except Exception as e:
            print(f"Error creating indexes: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_indexes() 