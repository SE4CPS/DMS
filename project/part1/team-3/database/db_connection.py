import psycopg2
import os
from dotenv import load_dotenv  # Create .env to store db url 
                                # Enhance security

# Load env variables
load_dotenv()

# Get db connection details from env var
db_url=os.getenv("database_url") 
print("Connection successful!")

def get_db_connection():
    try:
        return psycopg2.connect(db_url)
        
    except Exception as e:
        print("Error connecting to database: ", e)
        return None