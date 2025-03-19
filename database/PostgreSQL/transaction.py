import psycopg2

# PostgreSQL connection details
DATABASE_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

def execute_without_transaction():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print("Executing without transaction...")
        
        cur.execute("CREATE TABLE IF NOT EXISTS demo (id SERIAL PRIMARY KEY, value TEXT);")
        cur.execute("INSERT INTO demo (value) VALUES ('No Transaction 1');")
        cur.execute("INSERT INTO demo (value) VALUES ('No Transaction 2');")
        
        # Simulate an error
        cur.execute("INSERT INTO demo (value) VALUES ('No Transaction ' || 1/0);")
        
        conn.commit()  # This is never reached due to the error above
        cur.close()
        conn.close()
    except Exception as e:
        print("Error without transaction:", e)

def execute_with_transaction():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print("Executing with transaction...")
        
        cur.execute("CREATE TABLE IF NOT EXISTS demo (id SERIAL PRIMARY KEY, value TEXT);")
        
        try:
            cur.execute("BEGIN;")
            cur.execute("INSERT INTO demo (value) VALUES ('With Transaction 1');")
            cur.execute("INSERT INTO demo (value) VALUES ('With Transaction 2');")
            
            # Simulate an error
            cur.execute("INSERT INTO demo (value) VALUES ('With Transaction ' || 1/0);")
            
            conn.commit()  # This is never reached due to the error
        except Exception as e:
            conn.rollback()
            print("Transaction rolled back due to:", e)
        
        cur.close()
        conn.close()
    except Exception as e:
        print("Error with transaction:", e)

if __name__ == "__main__":
    execute_without_transaction()
    execute_with_transaction()
