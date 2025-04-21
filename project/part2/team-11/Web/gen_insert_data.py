# gen_insert_data.py

import sqlite3
from faker import Faker
import random

def generate_data():
    fake = Faker()
    conn = sqlite3.connect("../team11_flowers.db")
    cursor = conn.cursor()

    """ Insert ~100,000 customers """ 
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
    for _ in range(100000):
        name = fake.name()
        email = fake.user_name() + "@" + random.choice(domains)
        cursor.execute("INSERT INTO team11_customers (name, email) VALUES (?, ?)", (name, email))
    
    conn.commit()

    """ Get valid ID range """
    cursor.execute("SELECT MIN(id), MAX(id) FROM team11_customers")
    min_id, max_id = cursor.fetchone()

    """ Get number of flowers """
    cursor.execute("SELECT id FROM team11_flowers")
    flower_ids = [row[0] for row in cursor.fetchall()]

    """ Insert ~500,000 orders using available flower IDs """
    for _ in range(500000):
        customer_id = random.randint(min_id, max_id)
        flower_id = random.choice(flower_ids)
        order_date = fake.date()
        cursor.execute("INSERT INTO team11_orders (customer_id, flower_id, order_date) VALUES (?, ?, ?)",
                       (customer_id, flower_id, order_date))

    conn.commit()
    conn.close()

""" Allows script to be called directly """
if __name__ == "__main__":
    generate_data()
