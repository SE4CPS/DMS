from flask import Blueprint, request, jsonify
from database.db_connection import get_db_connection
import psycopg2

# Create Table: has been handle in different file.

# Update col table:

# Insert data
def insert_flowers():
    query = """
    INSERT INTO team3_flowers (flower_name, last_watered, water_level, min_water_required) 
    VALUES 
    ('Rose', '2024-02-10', 20, 5),
    ('Tulip', '2024-02-08', 10, 7),
    ('Lily', '2024-02-05', 3, 5);
    """
    
    # conn = db_connection.get_db_connection()
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
            print("Data  successfully inserted!")
        except Exception as e:
            print(f"Error inserting data: {e}")
        finally:
            conn.close()

# TEST 3 flowers:
# insert_flowers()

