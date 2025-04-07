import sqlite3 
from faker import Faker 
import random 

fake = Faker() 

""" 
Connect to the SQLite database
""" 
conn = sqlite3.connect("team11_flowers.db")
cursor = conn.cursor() 

"""
Generate and insert customers
""" 
for _ in range(102000):
    name = fake.name()
    email = fake.email()
    cursor.execute("INSERT INTO team11_customers (name, email) VALUES (?, ?)", (name, email))
    
"""
Generate and insert orders
""" 
for _ in range(501005):
    customer_id = random.randint(1, 102000)
    flower_id = random.randint(1, 3)
    order_date = fake.date()
    cursor.execute("INSERT INTO team11_orders (customer_id, flower_id, order_date) VALUES (?, ?, ?)", (customer_id, flower_id, order_date))
    
conn.commit()
conn.close()
