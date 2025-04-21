import psycopg2

conn = psycopg2.connect("postgresql://neondb_owner:npg_QuIm1wktTiV0@ep-nameless-base-aab6w7ti-pooler.westus3.azure.neon.tech/neondb?sslmode=require")
cur = conn.cursor()

with open('team7_customers.sql', 'r') as file:
    sql = file.read()
    cur.execute(sql)


#with open('team7_orders.sql', 'r') as file:
 #   sql = file.read()
  #  cur.execute(sql)

conn.commit()
cur.close()
conn.close()

print("Data has been inserted")
