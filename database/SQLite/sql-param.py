import sqlite3

DATABASE_FILE = "flowers.db"

def create_table():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS flowers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            );
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error creating table:", e)

# Vulnerable to SQL injection
def insert_flower_unsafe(flower_name):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        query = f"INSERT INTO flowers (name) VALUES ('{flower_name}');"
        print("Executing (unsafe):", query)
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error (unsafe):", e)

# Safe from SQL injection
def insert_flower_safe(flower_name):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        print("Executing (safe): INSERT INTO flowers (name) VALUES (?);", flower_name)
        cur.execute("INSERT INTO flowers (name) VALUES (?);", (flower_name,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error (safe):", e)

def show_flowers():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM flowers;")
        rows = cur.fetchall()
        print("Current Flowers:")
        for row in rows:
            print(row)
        cur.close()
        conn.close()
    except Exception as e:
        print("Error reading data:", e)

if __name__ == "__main__":
    create_table()
    show_flowers()

    # Normal input
    insert_flower_unsafe("Rose")

    # Injection that tries to drop the table
    insert_flower_unsafe("'); DROP TABLE flowers; --")

    # Injection that tries to delete all rows
    insert_flower_unsafe("'); DELETE FROM flowers; --")

    # Injection that tries to update a row
    insert_flower_unsafe("'); UPDATE flowers SET name = 'Hacked' WHERE id = 1; --")

    # Safe inputs (malicious strings are inserted as text)
    insert_flower_safe("Tulip")
    insert_flower_safe("'); DROP TABLE flowers; --")

    show_flowers()
