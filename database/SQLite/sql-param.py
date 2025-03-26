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

def insert_flower_unsafe(flower_name):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        print("Inserting (unsafe):", flower_name)
        cur.execute(f"INSERT INTO flowers (name) VALUES ('{flower_name}');")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error (unsafe):", e)

def insert_flower_safe(flower_name):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        print("Inserting (safe):", flower_name)
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

    # Simulate normal and malicious input
    insert_flower_unsafe("Rose")
    insert_flower_unsafe("'); DROP TABLE flowers; --")
    
    insert_flower_safe("Tulip")
    insert_flower_safe("'); DROP TABLE flowers; --")
    
    show_flowers()
