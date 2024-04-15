import sqlite3
import time
import os

# Function to create a SQLite database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create a table in the SQLite database
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT,
            model TEXT,
            year INTEGER
        )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Function to insert a record into the SQLite database
def insert_record(conn, make, model, year):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO vehicles (make, model, year)
        VALUES (?, ?, ?)
        """, (make, model, year))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(e)
        return None

# Function to read a record from the SQLite database
def read_record(conn, vehicle_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE id=?", (vehicle_id,))
        row = cursor.fetchone()
        return row
    except sqlite3.Error as e:
        print(e)
        return None

# Function to update a record in the SQLite database
def update_record(conn, vehicle_id, make=None, model=None, year=None):
    try:
        cursor = conn.cursor()
        update_query = "UPDATE vehicles SET"
        params = []
        if make is not None:
            update_query += " make=?,"
            params.append(make)
        if model is not None:
            update_query += " model=?,"
            params.append(model)
        if year is not None:
            update_query += " year=?,"
            params.append(year)
        # Remove the trailing comma and add the condition
        update_query = update_query.rstrip(',') + " WHERE id=?"
        params.append(vehicle_id)
        cursor.execute(update_query, tuple(params))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Function to delete a record from the SQLite database
def delete_record(conn, vehicle_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vehicles WHERE id=?", (vehicle_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Function to perform queries
def perform_queries(conn, count_queries):
    total_time = 0
    for i in range(count_queries):
        make = f"Make_{i}"
        model = f"Model_{i}"
        year = 2000 + i

        # Measure time for inserting a record
        start_time = time.time()
        vehicle_id = insert_record(conn, make, model, year)
        total_time += time.time() - start_time

        # Measure time for reading a record
        start_time = time.time()
        read_record(conn, vehicle_id)
        total_time += time.time() - start_time

        # Measure time for updating a record
        start_time = time.time()
        update_record(conn, vehicle_id, make=f"{make}_updated")
        total_time += time.time() - start_time

        # Measure time for deleting a record
        start_time = time.time()
        delete_record(conn, vehicle_id)
        total_time += time.time() - start_time

    return total_time

# Function to get the size of the SQLite database file
def get_database_size(db_file):
    if os.path.exists(db_file):
        return os.path.getsize(db_file) / (1024 * 1024)  # Convert bytes to megabytes
    else:
        return 0

# Main function
def main():
    database = "vehicle.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    # Create the vehicles table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT,
        model TEXT,
        year INTEGER
    )
    """)
    conn.commit()

    count_queries = 100

    # Perform queries
    total_time = perform_queries(conn, count_queries)
    print(f"Total Time for {count_queries} queries: {total_time} seconds")

    # Get the storage consumed by the database
    storage_consumption = get_database_size(database)
    print(f"Storage Consumption: {storage_consumption:.2f} MB")

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    main()
