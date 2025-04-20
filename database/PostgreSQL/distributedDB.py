import psycopg2
import sqlite3

# PostgreSQL connection string
DATABASE_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

# SQLite file
LOCAL_DB = "local_node.db"

def create_tables():
    # Remote PostgreSQL
    try:
        pg = psycopg2.connect(DATABASE_URL)
        pg.autocommit = True
        cur = pg.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS demo (id SERIAL PRIMARY KEY, value TEXT);")
        cur.close()
        pg.close()
    except Exception as e:
        print("Error creating table in PostgreSQL:", e)

    # Local SQLite
    try:
        conn = sqlite3.connect(LOCAL_DB)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS demo (id INTEGER PRIMARY KEY AUTOINCREMENT, value TEXT);")
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error creating table in SQLite:", e)

def replicate_to_both(value):
    # Insert into PostgreSQL
    try:
        pg = psycopg2.connect(DATABASE_URL)
        pg.autocommit = True
        cur = pg.cursor()
        cur.execute("INSERT INTO demo (value) VALUES (%s);", (value,))
        cur.close()
        pg.close()
        print("Inserted to PostgreSQL:", value)
    except Exception as e:
        print("PostgreSQL insert failed:", e)

    # Insert into SQLite
    try:
        conn = sqlite3.connect(LOCAL_DB)
        cur = conn.cursor()
        cur.execute("INSERT INTO demo (value) VALUES (?);", (value,))
        conn.commit()
        conn.close()
        print("Inserted to SQLite:", value)
    except Exception as e:
        print("SQLite insert failed:", e)

def insert_by_flower_type(flower_type, value):
    if flower_type == "Rose":
        # Insert into SQLite
        try:
            conn = sqlite3.connect(LOCAL_DB)
            cur = conn.cursor()
            cur.execute("INSERT INTO demo (value) VALUES (?);", (value,))
            conn.commit()
            conn.close()
            print(f"Inserted to SQLite (Rose): {value}")
        except Exception as e:
            print("SQLite insert failed:", e)
    else:
        # Insert into PostgreSQL
        try:
            pg = psycopg2.connect(DATABASE_URL)
            pg.autocommit = True
            cur = pg.cursor()
            cur.execute("INSERT INTO demo (value) VALUES (%s);", (value,))
            cur.close()
            pg.close()
            print(f"Inserted to PostgreSQL ({flower_type}): {value}")
        except Exception as e:
            print("PostgreSQL insert failed:", e)

def query_all_merged():
    print("\n--- Aggregated View ---")
    results = []
    try:
        pg = psycopg2.connect(DATABASE_URL)
        cur = pg.cursor()
        cur.execute("SELECT value FROM demo;")
        results += [f"PostgreSQL: {row[0]}" for row in cur.fetchall()]
        cur.close()
        pg.close()
    except Exception as e:
        print("PostgreSQL read failed:", e)

    try:
        conn = sqlite3.connect(LOCAL_DB)
        cur = conn.cursor()
        cur.execute("SELECT value FROM demo;")
        results += [f"SQLite: {row[0]}" for row in cur.fetchall()]
        conn.close()
    except Exception as e:
        print("SQLite read failed:", e)

    for r in results:
        print(r)

def read_with_fallback(record_id):
    try:
        pg = psycopg2.connect(DATABASE_URL)
        cur = pg.cursor()
        cur.execute("SELECT value FROM demo WHERE id = %s;", (record_id,))
        result = cur.fetchone()
        cur.close()
        pg.close()
        print(f"From PostgreSQL: {result[0]}")
    except:
        print("PostgreSQL failed, trying SQLite...")
        try:
            conn = sqlite3.connect(LOCAL_DB)
            cur = conn.cursor()
            cur.execute("SELECT value FROM demo WHERE id = ?;", (record_id,))
            result = cur.fetchone()
            conn.close()
            print(f"From SQLite: {result[0]}")
        except:
            print("Record not found on either node.")

def sync_sqlite_to_postgres():
    print("\n--- Syncing SQLite to PostgreSQL ---")
    try:
        conn = sqlite3.connect(LOCAL_DB)
        cur = conn.cursor()
        cur.execute("SELECT value FROM demo;")
        rows = cur.fetchall()
        conn.close()
    except Exception as e:
        print("SQLite read failed:", e)
        return

    try:
        pg = psycopg2.connect(DATABASE_URL)
        pg.autocommit = True
        cur = pg.cursor()
        for row in rows:
            cur.execute("INSERT INTO demo (value) VALUES (%s);", (row[0],))
            print(f"Synced: {row[0]}")
        cur.close()
        pg.close()
    except Exception as e:
        print("PostgreSQL write failed:", e)

def show_all_data():
    print("\n--- Remote PostgreSQL Data ---")
    try:
        pg = psycopg2.connect(DATABASE_URL)
        cur = pg.cursor()
        cur.execute("SELECT * FROM demo;")
        for row in cur.fetchall():
            print(row)
        cur.close()
        pg.close()
    except Exception as e:
        print("Error reading from PostgreSQL:", e)

    print("\n--- Local SQLite Data ---")
    try:
        conn = sqlite3.connect(LOCAL_DB)
        cur = conn.cursor()
        cur.execute("SELECT * FROM demo;")
        for row in cur.fetchall():
            print(row)
        conn.close()
    except Exception as e:
        print("Error reading from SQLite:", e)

if __name__ == "__main__":
    create_tables()
    replicate_to_both("Flower: Rose 🌹")
    replicate_to_both("Flower: Tulip 🌷")
    replicate_to_both("Flower: Daisy 🌼")
    insert_by_flower_type("Rose", "Rose - Red")
    insert_by_flower_type("Tulip", "Tulip - Yellow")
    insert_by_flower_type("Daisy", "Daisy - White")
    insert_by_flower_type("Rose", "Rose - Pink")
    query_all_merged()
    read_with_fallback(1)
    sync_sqlite_to_postgres()

    # show_all_data()