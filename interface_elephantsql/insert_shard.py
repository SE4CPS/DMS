import psycopg2

# List of database connection strings (representing different shards)
DATABASE_URLS = [
    "postgres://pbcusqgz:glJ53RAC-vj2evae_dZVSPnQqI8e_Nui@bubble.db.elephantsql.com/pbcusqgz",
    "postgres://hzypcrnd:5jE78MKpt6885VDIbxRkuI0aBteqqpey@bubble.db.elephantsql.com/hzypcrnd",
    "postgres://nchemrjv:CRSus5sf-6lyOuVx7987xohUWIymuo34@bubble.db.elephantsql.com/nchemrjv"
]

# Function to choose a shard based on the bike price
def choose_shard_by_price(bike_price, db_urls):
    # Example price ranges for demonstration: [0-1000), [1000, 2000), [2000+]
    if bike_price < 1000:
        return db_urls[0]  # First shard for lower-priced bikes
    elif bike_price < 2000:
        return db_urls[1]  # Second shard for mid-priced bikes
    else:
        return db_urls[2]  # Third shard for higher-priced bikes

# Function to insert a bike into the appropriate shard based on its price
def insert_bike_into_shard_by_price(bike_data, db_urls):
    bike_model, bike_price = bike_data
    # Determine the appropriate shard for this bike based on its price
    shard_url = choose_shard_by_price(bike_price, db_urls)
    
    insert_command = """
    INSERT INTO bike (bike_model, bike_price) VALUES (%s, %s)
    """
    
    try:
        # Connect to the selected database
        conn = psycopg2.connect(shard_url)
        cur = conn.cursor()
        
        # Insert the bike into the table
        cur.execute(insert_command, (bike_model, bike_price))
        
        # Commit the changes
        conn.commit()
        
        print(f"Bike '{bike_model}' with price ${bike_price} inserted successfully into shard: {shard_url}")
        
    except psycopg2.DatabaseError as e:
        print(f"An error occurred with database {shard_url}: {e}")
    finally:
        # Ensure that the database connection is closed
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

# Example bikes to insert, demonstrating various prices
bikes_to_insert = [
    ('Mountain Bike', 500.00),
    ('Road Bike', 1500.00),
    ('Hybrid Bike', 800.00),
    ('Electric Bike', 2500.00),
    ('Kids Bike', 200.00)
]

# Insert each bike into the appropriate shard based on price
for bike in bikes_to_insert:
    insert_bike_into_shard_by_price(bike, DATABASE_URLS)
