import psycopg2

DATABASE_URLS = {
    'public': "postgres://hzypcrnd:5jE78MKpt6885VDIbxRkuI0aBteqqpey@bubble.db.elephantsql.com/hzypcrnd",
    'private': "postgres://nchemrjv:CRSus5sf-6lyOuVx7987xohUWIymuo34@bubble.db.elephantsql.com/nchemrjv"
}

def insert_bike_into_both_databases(bike_data):

    bike_model, bike_price = bike_data
    
    # Define the insert command template
    insert_command = """
    INSERT INTO bike (bike_model, bike_price) VALUES (%s, %s)
    """
    
    for role, database_url in DATABASE_URLS.items():
        try:
            # Connect to the database
            conn = psycopg2.connect(database_url)
            cur = conn.cursor()
            
            # Insert the bike into the table, adjusting price visibility based on the role
            if role == 'public':
                values = ( )
            else:
                values = ( )
            
            # Execute the insert command
            cur.execute(insert_command, values)
            conn.commit()
            print(f"Bike '{bike_model}' inserted successfully into {role} database.")
        
        except psycopg2.DatabaseError as e:
            print(f"An error occurred with the {role} database: {e}")
        finally:
            # Ensure that the database connection is closed
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

bikes_to_insert = [
    ('Mountain Bike', 500.00),
    ('Road Bike', 1500.00),
    ('Hybrid Bike', 800.00),
    ('Electric Bike', 2500.00),
    ('Kids Bike', 200.00)
]

for bike in bikes_to_insert:
    insert_bike_into_both_databases(bike)