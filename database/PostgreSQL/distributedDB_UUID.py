import psycopg2
import sqlite3
import uuid

# PostgreSQL connection string (remote)
DATABASE_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

# SQLite local database file
LOCAL_DB = "local_flowers.db"

def create_tables():
    # PostgreSQL
    try:
        pg = psycopg2.connect(DATABASE_URL)
        pg.autocommit = True
        cur = pg.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS demo (
                id SERIAL PRIMARY KEY,
                uuid TEXT,
                value TEXT
            );
        """)
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='demo' AND column_name='uuid';")
        has_uuid = cur.fetchone()
        if not has_uuid:
            print("🔧 'uuid' column missing in PostgreSQL. Recreating table.")
            cur.execute("DROP TABLE IF EXISTS demo;")
            cur.execute("""
                CREATE TABLE demo (
                    id SERIAL PRIMARY KEY,
                    uuid TEXT,
                    value TEXT
                );
            """)
        cur.close()
        pg.close()
        print("✅ PostgreSQL table ready.")
    except Exception as e:
        print("❌ Error creating PostgreSQL table:", e)

    # SQLite
    try:
        conn = sqlite3.connect(LOCAL_DB)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS demo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid TEXT,
                value TEXT
            );
        """)
        conn.commit()
        conn.close()
        print("✅ SQLite table ready.")
    except Exception as e:
        print("❌ Error creating SQLite table:", e)

def insert_with_uuid(flower_type, value):
    flower_uuid = str(uuid.uuid4())

    if flower_type.lower() == "rose":
        # Local SQLite insert
        try:
            conn = sqlite3.connect(LOCAL_DB)
            cur = conn.cursor()
            cur.execute("INSERT INTO demo (uuid, value) VALUES (?, ?);", (flower_uuid, value))
            conn.commit()
            conn.close()
            print(f"[SQLite] Inserted {flower_type} with UUID: {flower_uuid}")
        except Exception as e:
            print("❌ SQLite insert failed:", e)
    else:
        # Remote PostgreSQL insert
        try:
            pg = psycopg2.connect(DATABASE_URL)
            pg.autocommit = True
            cur = pg.cursor()
            cur.execute("INSERT INTO demo (uuid, value) VALUES (%s, %s);", (flower_uuid, value))
            cur.close()
            pg.close()
            print(f"[PostgreSQL] Inserted {flower_type} with UUID: {flower_uuid}")
        except Exception as e:
            print("❌ PostgreSQL insert failed:", e)

    return flower_uuid

def lookup_by_uuid(flower_uuid):
    print(f"\n🔍 Looking up flower with UUID: {flower_uuid}")

    # PostgreSQL
    try:
        pg = psycopg2.connect(DATABASE_URL)
        cur = pg.cursor()
        cur.execute("SELECT value FROM demo WHERE uuid = %s;", (flower_uuid,))
        result = cur.fetchone()
        cur.close()
        pg.close()
        if result:
            print(f"[PostgreSQL] Found: {result[0]}")
        else:
            print("[PostgreSQL] Not found.")
    except Exception as e:
        print("❌ PostgreSQL lookup failed:", e)

    # SQLite
    try:
        conn = sqlite3.connect(LOCAL_DB)
        cur = conn.cursor()
        cur.execute("SELECT value FROM demo WHERE uuid = ?;", (flower_uuid,))
        result = cur.fetchone()
        conn.close()
        if result:
            print(f"[SQLite] Found: {result[0]}")
        else:
            print("[SQLite] Not found.")
    except Exception as e:
        print("❌ SQLite lookup failed:", e)

if __name__ == "__main__":
    create_tables()

    print("\n🌸 Inserting flower records:")
    uuid1 = insert_with_uuid("Rose", "Rose - Red")
    uuid2 = insert_with_uuid("Tulip", "Tulip - Yellow")

    print("\n🔎 Performing UUID lookups:")
    lookup_by_uuid(uuid1)
    lookup_by_uuid(uuid2)