import psycopg2

conn = psycopg2.connect("postgresql://neondb_owner:npg_QuIm1wktTiV0@ep-nameless-base-aab6w7ti-pooler.westus3.azure.neon.tech/neondb?sslmode=require")
cur = conn.cursor()

# Query the orders table
cur.execute("SELECT * FROM team7_orders;")
orders = cur.fetchall()
print("Orders:", orders)

# Query the customers table
cur.execute("SELECT * FROM team7_customers;")
customers = cur.fetchall()
print("Customers:", customers)

cur.close()
conn.close()
