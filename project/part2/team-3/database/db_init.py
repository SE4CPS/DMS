from db_connection import get_db_connection

def db_init():
    conn=get_db_connection()
    if conn:
        cur=conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS team3_flowers(
                flower_id SERIAL PRIMARY KEY,
                flower_name TEXT NOT NULL,
                last_watered DATE NOT NULL CHECK(last_watered <= CURRENT_DATE),
                water_level INT NOT NULL CHECK(water_level >= 0),
                min_water_required INT NOT NULL CHECK(min_water_required >= 0) 
            );
            """
        )
        
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS team3_customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            );
            """
        )
        
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS team3_orders (
                id SERIAL PRIMARY KEY,
                customer_id INT REFERENCES team3_customers(id),
                flower_id INT REFERENCES team3_flowers(flower_id),
                order_date DATE
            );
            """
        )
        
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS team3_customers_encrypted (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email BYTEA  -- For storing encrypted data
            );
            """
        )
        
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS team3_orders_encrypted (
                id SERIAL PRIMARY KEY,
                customer_id INT REFERENCES team3_customers_encrypted(id),
                flower_id INT REFERENCES team3_flowers(flower_id),
                order_date BYTEA  -- For storing encrypted data
            );
            """
        )
        
        conn.commit()
        cur.close()
        conn.close()
        print("Initialize database.")   
        
def update_col():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            ALTER TABLE team3_flowers
            ADD CONSTRAINT water_level CHECK(water_level >= 0);
            """
        )
        
        cur.execute(
            """
            ALTER TABLE team3_flowers
            ADD CONSTRAINT last_watered CHECK(last_watered <= CURRENT_DATE);
            """
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Table altered successfully with new constraints.")
        
    except Exception as e:
        print("Error altering table:", e)
        
def clean_invalid_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            DELETE FROM team3_flowers WHERE water_level < 0;
            DELETE FROM team3_flowers WHERE last_watered > CURRENT_DATE;
            """
        )
        
        conn.commit()
        print("Invalid data removed successfully.")
        cur.close()
        conn.close()


    except Exception as e:
        print("Error cleaning data: ", e)
    
if __name__ == "__main__":
        # db_init()
        # update_col()
        clean_invalid_data()
    