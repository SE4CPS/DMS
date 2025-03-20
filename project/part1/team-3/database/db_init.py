from db_connection import get_db_connection

def init_db():
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
