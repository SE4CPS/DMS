import psycopg2

# List of database connection strings
DATABASE_URLS = [
    "postgres://pbcusqgz:glJ53RAC-vj2evae_dZVSPnQqI8e_Nui@bubble.db.elephantsql.com/pbcusqgz",
    "postgres://hzypcrnd:5jE78MKpt6885VDIbxRkuI0aBteqqpey@bubble.db.elephantsql.com/hzypcrnd",
    "postgres://nchemrjv:CRSus5sf-6lyOuVx7987xohUWIymuo34@bubble.db.elephantsql.com/nchemrjv"
]

# Function to connect to a database and fetch its version
def fetch_db_version(db_url):
    try:
        # Connect to the database
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Execute a query to get the PostgreSQL version
        cur.execute("SELECT version();")
        
        # Fetch and print the result
        version = cur.fetchone()
        print(f"Database {db_url} PostgreSQL version: {version[0]}")
        
    except psycopg2.DatabaseError as error:
        print(f"Error with database {db_url}: {error}")
    finally:
        # Ensure that the cursor and connection are closed
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

# Iterate over the database URLs and fetch their PostgreSQL version
for db_url in DATABASE_URLS:
    fetch_db_version(db_url)