import psycopg2

# List of database connection strings
DATABASE_URLS = [
    "postgres://pbcusqgz:glJ53RAC-vj2evae_dZVSPnQqI8e_Nui@bubble.db.elephantsql.com/pbcusqgz",
    "postgres://hzypcrnd:5jE78MKpt6885VDIbxRkuI0aBteqqpey@bubble.db.elephantsql.com/hzypcrnd",
    "postgres://nchemrjv:CRSus5sf-6lyOuVx7987xohUWIymuo34@bubble.db.elephantsql.com/nchemrjv"
]

# Bikes to insert
bikes_to_insert = [
    ('Mountain Bike', 500.00),
    ('Road Bike', 700.00),
    ('Hybrid Bike', 300.00),
    ('Electric Bike', 2500.00),
    ('Kids Bike', 150.00)
]

insert_command = """
INSERT INTO bike (bike_model, bike_price) VALUES (%s, %s)
"""

# Function to insert bikes into a given database
def insert_bikes_into_database(db_url):
    try:
        # Connect to the database using the database URL
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Insert bikes into the table
        cur.executemany(insert_command, bikes_to_insert)
        
        # Commit the changes
        conn.commit()
        
        print(f"5 bikes inserted successfully into database: {db_url}")
        
    except psycopg2.DatabaseError as e:
        print(f"An error occurred in database {db_url}: {e}")
    finally:
        # Ensure that the database connection is closed
        if cur: cur.close()
        if conn: conn.close()

# Iterate over each database URL and insert the bikes
for db_url in DATABASE_URLS:
    insert_bikes_into_database(db_url)