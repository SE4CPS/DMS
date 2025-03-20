import psycopg2

# PostgreSQL connection details
DATABASE_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

def create_table():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True  # Enable autocommit
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS demo (id SERIAL PRIMARY KEY, value TEXT);")
        cur.close()
        conn.close()
    except Exception as e:
        print("Error creating table:", e)

def execute_without_transaction():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True  # Enable autocommit
        cur = conn.cursor()
        print("Executing without transaction...")
        
        cur.execute("INSERT INTO demo (value) VALUES ('No Transaction 1');")
        cur.execute("INSERT INTO demo (value) VALUES ('No Transaction 2');")
        
        # Simulate an error
        raise ValueError("Simulated error for transaction rollback")
        
        cur.close()
        conn.close()
    except Exception as e:
        print("Error without transaction:", e)

def execute_with_transaction():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print("Executing with transaction...")
        
        try:
            cur.execute("BEGIN;")
            cur.execute("INSERT INTO demo (value) VALUES ('With Transaction 1');")
            cur.execute("INSERT INTO demo (value) VALUES ('With Transaction 2');")
            
            # Simulate an error
            raise ValueError("Simulated error for transaction rollback")
            
            conn.commit()  # This is never reached due to the error
        except Exception as e:
            conn.rollback()
            print("Transaction rolled back due to:", e)
        
        cur.close()
        conn.close()
    except Exception as e:
        print("Error with transaction:", e)

def show_data():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True  # Enable autocommit
        cur = conn.cursor()
        cur.execute("SELECT * FROM demo;")
        rows = cur.fetchall()
        print("Current Data in 'demo' Table:")
        for row in rows:
            print(row)
        cur.close()
        conn.close()
    except Exception as e:
        print("Error retrieving data:", e)

if __name__ == "__main__":
    create_table()
    show_data()
    execute_without_transaction()
    show_data()
    execute_with_transaction()
    show_data()