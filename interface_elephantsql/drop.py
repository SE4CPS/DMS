import psycopg2

# List of database connection strings (representing different databases)
DATABASE_URLS = [
    "postgres://pbcusqgz:glJ53RAC-vj2evae_dZVSPnQqI8e_Nui@bubble.db.elephantsql.com/pbcusqgz",
    "postgres://hzypcrnd:5jE78MKpt6885VDIbxRkuI0aBteqqpey@bubble.db.elephantsql.com/hzypcrnd",
    "postgres://nchemrjv:CRSus5sf-6lyOuVx7987xohUWIymuo34@bubble.db.elephantsql.com/nchemrjv"
]

drop_table_command = """
DROP TABLE IF EXISTS bike
"""

# Function to drop the 'bike' table in a specific database
def drop_table_in_database(db_url):
    try:
        # Connect to the database
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Drop the 'bike' table
        cur.execute(drop_table_command)
        
        # Commit the changes
        conn.commit()
        
        print(f"Bikes table dropped successfully in database: {db_url}")
        
    except psycopg2.DatabaseError as e:
        print(f"An error occurred with database {db_url}: {e}")
    finally:
        # Ensure that the database connection is closed
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

# Iterate over each database URL and drop the 'bike' table
for db_url in DATABASE_URLS:
    drop_table_in_database(db_url)