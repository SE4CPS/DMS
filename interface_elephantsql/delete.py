import psycopg2

# List of database connection strings
DATABASE_URLS = [
    "postgres://pbcusqgz:glJ53RAC-vj2evae_dZVSPnQqI8e_Nui@bubble.db.elephantsql.com/pbcusqgz",
    "postgres://hzypcrnd:5jE78MKpt6885VDIbxRkuI0aBteqqpey@bubble.db.elephantsql.com/hzypcrnd",
    "postgres://nchemrjv:CRSus5sf-6lyOuVx7987xohUWIymuo34@bubble.db.elephantsql.com/nchemrjv"
]

delete_command = """
DELETE FROM bike
"""

# Function to delete all bikes from a specific database
def delete_bikes_from_database(db_url):
    try:
        # Connect to the database
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Delete all bikes from the table
        cur.execute(delete_command)
        
        # Commit the changes
        conn.commit()
        
        print(f"All bikes deleted successfully from database: {db_url}")
        
    except psycopg2.DatabaseError as e:
        print(f"An error occurred with database {db_url}: {e}")
    finally:
        # Ensure that the database connection is closed
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

# Iterate over each database URL and delete the bikes
for db_url in DATABASE_URLS:
    delete_bikes_from_database(db_url)