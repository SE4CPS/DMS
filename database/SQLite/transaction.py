import sqlite3

# SQLite database file
DATABASE_FILE = "example.db"

def create_table():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.execute("PRAGMA journal_mode=WAL;")  # Enable Write-Ahead Logging for better concurrency
        conn.execute("CREATE TABLE IF NOT EXISTS demo (id INTEGER PRIMARY KEY AUTOINCREMENT, value TEXT);")
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error creating table:", e)

def execute_without_transaction():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.isolation_level = None  # Enable autocommit
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
        conn = sqlite3.connect(DATABASE_FILE)
        conn.isolation_level = None  # Disable autocommit to manually control transactions
        cur = conn.cursor()
        print("Executing with transaction...")
        
        try:
            conn.execute("BEGIN;")  # Ensure full transaction control
            cur.execute("INSERT INTO demo (value) VALUES ('With Transaction 1');")
            cur.execute("INSERT INTO demo (value) VALUES ('With Transaction 2');")
            
            # Simulate an error
            raise ValueError("Simulated error for transaction rollback")
            
            conn.commit()  # This is never reached due to the error
        except Exception as e:
            conn.rollback()  # Rollback the entire transaction
            print("Transaction rolled back due to:", e)
        
        cur.close()
        conn.close()
    except Exception as e:
        print("Error with transaction:", e)

def show_data():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
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