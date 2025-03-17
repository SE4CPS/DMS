from dotenv import load_dotenv, dotenv_values
import psycopg2
import os

# Input the absolute path to the .env file
load_dotenv()

# AWS PostgreSQL connection
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_URI')}:5432/{os.getenv('DB_NAME')}"

# change flowerTest to team1_flowers after testing is sucessful
try:
    # Connect to PostgreSQL database
    def get_db_connection():
        return psycopg2.connect(DATABASE_URL)

except Exception as e:
    print("Error:", e)