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
                last_watered DATE NOT NULL,
                water_level INT NOT NULL,
                min_water_required INT NOT NULL  
            );
            """
        )
        
        conn.commit()
        cur.close()
        conn.close()
        print("Initialize database.")
        
if __name__ == "__main__":
        db_init()
