from dotenv import load_dotenv, dotenv_values
import psycopg2
import os

# Input the absolute path to the .env file
load_dotenv()

# AWS PostgreSQL connection
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_URI')}:5432/{os.getenv('DB_NAME')}"

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True  # Enable auto-commit for transactions
    print("Connected to PostgreSQL successfully!\n")

    # Create a cursor object
    cur = conn.cursor()

    # Retrieve all flowers
    cur.execute("SELECT * FROM flowers;")
    flower_data = cur.fetchall()

    # Get column names
    col_names = [desc[0] for desc in cur.description]

    # Print table header
    print(f"{col_names[0]:<10} {col_names[1]:<20} {col_names[2]:<15} {col_names[3]:<10} {col_names[4]:<10}")
    print("-" * 65)

    # Print rows
    for row in flower_data:
        print(f"{row[0]:<10} {row[1]:<20} {row[2]:<15} {row[3]:<10.2f} {row[4]:<10}")

    # Close cursor and connection
    cur.close()
    conn.close()
    print("\nConnection closed.")

except Exception as e:
    print("Error:", e)