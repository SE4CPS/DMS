from dotenv import load_dotenv, dotenv_values
import psycopg2
import os

# Input the absolute path to the .env file
load_dotenv("/Users/parneet.kheira/Desktop/comp163/water_run_env/water_run.env")

# AWS PostgreSQL connection
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_URI')}:5432/{os.getenv('DB_NAME')}"

try:
    # Connect to PostgreSQL database
    def get_db_connection():
        return psycopg2.connect(DATABASE_URL)
except Exception as e:
    print("Error:", e)

# Query Functions

# Retrieving flowers that need to be watered
def need_to_be_watered_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flower WHERE current_water_level_in_inches < minimum_water_level_in_inches")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return flowers

# Retrieving flowers that are outdoor
def outdoor_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flower WHERE environment = 'outdoor'")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return flowers

# Retrieving flowers that are indoor
def indoor_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flower WHERE environment = 'indoor'")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return flowers

# Retrieving all files
def manage_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flower ORDER BY flower_id") # Specifying the order of ALL the flowers
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return flowers

# Retrieving all flowers (flower_id and name)
def watering_flowers_helper():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT flower_id, name,current_water_level_in_inches,minimum_water_level_in_inches FROM flower ORDER BY flower_id") # Specifying the order of ALL the flowers
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return flowers

# Adds 10 inches of water to all outdoor flowers
def water_outdoor_flowers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE flower SET current_water_level_in_inches = current_water_level_in_inches + 10 WHERE environment = 'outdoor'")
    cur.execute("UPDATE flower SET last_watered = current_timestamp WHERE environment = 'outdoor'")
    conn.commit()
    cur.close()
    conn.close()

# Removes selected flowers from the database
def remove_selected_flower(flower_ids):
    if not flower_ids:
        return
    conn = get_db_connection()
    cur = conn.cursor()

    format_strings = ','.join(['%s'] * len(flower_ids))
    query = f"DELETE FROM flower WHERE flower_id IN ({format_strings})"

    cur.execute(query, tuple(flower_ids))
    conn.commit()
    cur.close()
    conn.close()