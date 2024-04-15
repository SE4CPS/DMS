import psycopg2
import os
import time

# Function to create a PostgreSQL database connection
def create_connection(db_url):
    conn = None
    try:
        conn = psycopg2.connect(db_url)
        return conn
    except psycopg2.Error as e:
        print(e)
    return conn

# Function to create a table in the PostgreSQL database
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id SERIAL PRIMARY KEY,
            make TEXT,
            model TEXT,
            year INTEGER
        )
        """)
        conn.commit()
    except psycopg2.Error as e:
        print(e)

# Function to insert a record into the PostgreSQL database
def insert_record(conn, make, model, year):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO vehicles (make, model, year)
        VALUES (%s, %s, %s)
        """, (make, model, year))
        conn.commit()
    except psycopg2.Error as e:
        print(e)

# Function to read a record from the PostgreSQL database
def read_record(conn, vehicle_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE id=%s", (vehicle_id,))
        row = cursor.fetchone()
        return row
    except psycopg2.Error as e:
        print(e)

# Function to update a record in the PostgreSQL database
def update_record(conn, vehicle_id, make=None, model=None, year=None):
    try:
        cursor = conn.cursor()
        update_query = "UPDATE vehicles SET"
        params = []
        if make is not None:
            update_query += " make=%s,"
            params.append(make)
        if model is not None:
            update_query += " model=%s,"
            params.append(model)
        if year is not None:
            update_query += " year=%s,"
            params.append(year)
        # Remove the trailing comma and add the condition
        update_query = update_query.rstrip(',') + " WHERE id=%s"
        params.append(vehicle_id)
        cursor.execute(update_query, tuple(params))
        conn.commit()
    except psycopg2.Error as e:
        print(e)

# Function to delete a record from the PostgreSQL database
def delete_record(conn, vehicle_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vehicles WHERE id=%s", (vehicle_id,))
        conn.commit()
    except psycopg2.Error as e:
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
        insert_record(conn, make, model, year)
        total_time += time.time() - start_time

        # Measure time for reading a record
        start_time = time.time()
        read_record(conn, i+1)
        total_time += time.time() - start_time

        # Measure time for updating a record
        start_time = time.time()
        update_record(conn, i+1, make=f"{make}_updated")
        total_time += time.time() - start_time

        # Measure time for deleting a record
        start_time = time.time()
        delete_record(conn, i+1)
        total_time += time.time() - start_time

    return total_time

# Function to get the size of the PostgreSQL database
def get_database_size(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()));")
        size = cursor.fetchone()[0]
        return size
    except psycopg2.Error as e:
        print(e)

# Main function
def main():
    DATABASE_URLS = [
        "postgres://pbcusqgz:glJ53RAC-vj2evae_dZVSPnQqI8e_Nui@bubble.db.elephantsql.com/pbcusqgz"
    ]

    for db_url in DATABASE_URLS:
        print(f"Database URL: {db_url}")

        conn = create_connection(db_url)

        if conn is not None:
            create_table(conn)
            count_queries = 100

            # Perform queries
            total_time = perform_queries(conn, count_queries)
            print(f"Total Time for {count_queries} queries: {total_time} seconds")

            # Get the size of the database
            database_size = get_database_size(conn)
            print(f"Database Size: {database_size}")

            # Close the database connection
            conn.close()

            print()  # Add a blank line for better readability
        else:
            print("Error! Unable to create database connection.")

if __name__ == '__main__':
    main()
