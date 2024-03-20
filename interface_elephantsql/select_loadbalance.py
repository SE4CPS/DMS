import psycopg2
import datetime

# List of database connection strings
DATABASE_URLS = [
    "postgres://pbcusqgz:glJ53RAC-vj2evae_dZVSPnQqI8e_Nui@bubble.db.elephantsql.com/pbcusqgz",
    "postgres://hzypcrnd:5jE78MKpt6885VDIbxRkuI0aBteqqpey@bubble.db.elephantsql.com/hzypcrnd",
    "postgres://nchemrjv:CRSus5sf-6lyOuVx7987xohUWIymuo34@bubble.db.elephantsql.com/nchemrjv"
]

# SQL command to query all entries from the "bike" table
query_command = "SELECT bike_id, bike_model, bike_price FROM bike"

def query_database_rotating(db_urls, query):
    # Determine the starting index based on current time
    start_index = datetime.datetime.now().second % len(db_urls)
    
    # Rotate the database URLs to start with the chosen one
    rotated_urls = db_urls[start_index:] + db_urls[:start_index]
    
    for db_url in rotated_urls:
        try:
            # Connect to the database
            conn = psycopg2.connect(db_url)
            cur = conn.cursor()
            
            # Execute the query
            cur.execute(query)
            
            # Fetch all rows from the table
            rows = cur.fetchall()
            if rows:
                # Indicate which database was picked and show the data
                print(f"Data retrieved from database URL: {db_url}")
                for row in rows:
                    print(f"Bike ID: {row[0]}, Model: {row[1]}, Price: ${row[2]}")
                # Stop after successful read
                break
            else:
                # If no data found, log and move to the next database
                print(f"No data found in database: {db_url}")
            
        except psycopg2.DatabaseError as e:
            print(f"An error occurred with database {db_url}: {e}")
        finally:
            # Ensure that the database connection is closed
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

# Query databases with rotation
query_database_rotating(DATABASE_URLS, query_command)