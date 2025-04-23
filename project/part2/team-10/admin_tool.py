import psycopg2
import psycopg2.extras
import re
import random
import datetime

# names to autogenerate from
firstnames = []
with open('first-names.txt', 'r') as file:
    for line in file:
        firstnames.append(line.strip())

# names to autogenerate from
middlenames = []
with open('middle-names.txt', 'r') as file:
    for line in file:
        middlenames.append(line.strip())

# names to autogenerate from
lastnames = []
with open('last-names.txt', 'r') as file:
    for line in file:
        lastnames.append(line.strip().capitalize())

flowernames = []
with open('last-names.txt', 'r') as file:
    for line in file:
        flowernames.append(line.strip())

emailextensions=[
            '@gmail.com',
            '@aol.com',
            '@comcast.net',
            '@xfinity.com',
            '@pacific.edu',
            '@u.pacific.edu',
            '@yahoo.com',
            '@fakeemail.com'
        ]

# get postgresql url
print("Database Url: postgresql://neondb_owner:npg_K4PbdhY0oTuH@ep-sweet-river-a4g0qfek-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require")
DB_URL = "postgresql://neondb_owner:npg_K4PbdhY0oTuH@ep-sweet-river-a4g0qfek-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

def get_connection():
    try:
        print("   | Connecting..")
        conn = psycopg2.connect(DB_URL)
        conn.autocommit = True
        return conn
    except Exception as e:
        print("   | CONNECTION ERROR: ", e)

def execute(sql):
    conn = get_connection()
    print("   | Get DB cursor..")
    cur = conn.cursor()
    print("   | Executing: ", sql)

    try:
        cur.execute(sql)
        return(cur)
    except Exception as e:
        print("   | SQL EXECUTE ERROR: ", e)

def print_table(number):
    match number:
        case 1:
            table='team10_flowers'
        case 2:
            table='team10_customers'
        case 3:
            table='team10_orders'

    cur = execute('SELECT * FROM {};'.format(table))
    rows = cur.fetchall();

    for row in rows:
        print(row)

def create_tables():
    execute(
    """
    BEGIN;
    CREATE EXTENSION IF NOT EXISTS pgcrypto;
    CREATE TABLE team10_flowers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        last_watered DATE NOT NULL,
        water_level INT NOT NULL,
        min_water_required INT NOT NULL
    );
    UPDATE team10_flowers
    SET water_level = water_level - (5 * (CURRENT_DATE - last_watered));
    CREATE TABLE team10_customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    );
    CREATE TABLE team10_orders (
        id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES team10_customers(id),
        flower_id INT REFERENCES team10_flowers(id),
        order_date DATE
    );
    COMMIT;
    """
    )
def rebuild_tables():
    execute(
    """
    DROP TABLE team10_orders;
    DROP TABLE team10_flowers;
    DROP TABLE team10_customers;
    """
    )
    create_tables()
def fill_database():
    conn = get_connection()

    print("   | Get DB cursor..")
    cur = conn.cursor()

    print("   | Seeding Rand..")
    random.seed(pow(datetime.datetime.now().microsecond, 80158))

    print("   | Generating Random Users..")
    userstoadd=[]
    for i in range(100000):
        firstname=firstnames[random.randint(0, len(firstnames) - 1)]
        middlename=middlenames[random.randint(0, len(middlenames) - 1)]
        lastname=lastnames[random.randint(0, len(lastnames) - 1)]
        username='{}_{}_{}'.format(firstname, middlename, lastname)
        email=username + emailextensions[random.randint(0, len(emailextensions) - 1)]
        print('New User:\n|   {}\n|   {}\n'.format(username, email))
        userstoadd.append((username, email))


    print("   | Executing Batch Fill : Customers..")
    print("   | NOTE: may take awhile ~100,000 customers to add..")
    psycopg2.extras.execute_batch(
    cur,
    """
    INSERT INTO team10_customers
    VALUES (DEFAULT, %s, %s);
    """,
    userstoadd
    )

    print("   | Generating Random Flowers..")
    flowerstoadd = []
    for i in range(30):
        flowername = flowernames[random.randint(0, len(flowernames) - 1)]
        last_watered = datetime.date.today()
        water_level = random.randint(0, 10)
        min_water_required = random.randint(0, 5)
        print("New Flower:\n|   {}\n|   {}\n|   {}\n|   {}\n".format(flowername, last_watered, water_level, min_water_required))
        flowerstoadd.append((flowername, last_watered, water_level, min_water_required))

    print("   | Executing Batch Fill : Flowers..")
    psycopg2.extras.execute_batch(
            cur,
            """
            INSERT INTO team10_flowers
            VALUES (DEFAULT, %s, %s, %s, %s);
            """,
            flowerstoadd
    )

    print('   | Getting Flower Count..')
    res = execute(
        """
        SELECT COUNT(*) FROM team10_flowers;
        """
    )

    flowercount = (res.fetchall())[0][0]

    print('   | Generating Some Orders..')
    orderstoadd = []
    for i in range(500000):
        customer = random.randint(1, 100000)
        flower = random.randint(1, flowercount)
        date = datetime.date.today()
        print('New Order:\n|   {}\n|   {}\n|   {}\n'.format(customer, flower, date))
        orderstoadd.append((customer, flower, date))

    print("   | Executing Batch Fill : Orders..")
    print("   | NOTE: may take awhile ~500,000 orders to add..")
    psycopg2.extras.execute_batch(
            cur,
            """
            INSERT INTO team10_orders
            VALUES (DEFAULT, %s, %s, %s);
            """,
            orderstoadd
    )
    
    # close cursor
    print("   | Complete!")
    cur.close()

def print_schema():
    res = execute(
    """
    SELECT * FROM pg_tables;
    """
    )

    rows = res.fetchall()

    for row in rows:
        if (re.search("team10_.*", row[1])):
            print(row)

def slow_query():
    start_time = datetime.datetime.now()
    res = execute(
        """
        EXPLAIN ANALYZE
        SELECT *
        FROM team10_orders
        FULL JOIN team10_customers ON team10_orders.customer_id=team10_customers.id
        CROSS JOIN team10_flowers
        ORDER BY team10_flowers.name
        """
    ) #('Execution Time: 592.386 ms',)
    print('Duration: {}'.format(datetime.datetime.now() - start_time))

    rows = res.fetchall()
    for row in rows:
        for item in row:
            if (re.search(".*Execution Time:.*", item)):
                match = re.search("[0-9]*\.[0-9]*", item);
                seconds = round(float(item[match.span()[0]:match.span()[1]]) / 1000, 3)
                print('Execution Time: ', seconds)

def print_table_prompt():
    print("|----------------------------------|")
    print("| Options:                         |")
    print("|----------------------------------|")
    print("| f -> Flowers                     |")
    print("| c -> Customers                   |")
    print("| o -> Orders                      |")
    print("| b -> Back                        |")
    print("|----------------------------------|")

def table_data():
    print_table_prompt()
    user_table = input("Your Choice: ")

    while user_table != 'b':
        match user_table:
            case 'f':
                print_table(1)
                break;
            case 'c':
                print_table(2)
                break;
            case 'o':
                print_table(3)
                break;
            case _:
                print('Invalid Choice..')
                break;

        print_table_prompt()
        user_table = input("Your Choice: ")

def print_prompt():
    print("|----------------------------------|")
    print("| Admin Tool                       |")
    print("|----------------------------------|")
    print("| Options:                         |")
    print("|----------------------------------|")
    print("| c -> Create Tables in Postgresql |")
    print("| r -> Rebuild Tables              |")
    print("| f -> Fill Database with Data     |")
    print("| p -> Print Tables                |")
    print("| t -> Print table data            |")
    print("| h -> Print this prompt           |")
    print("|----------------------------------|")

print_prompt()
user_input = input("Your Choice: ")

while user_input != 'q':
    # inform user
    print_prompt()

    # check previous input
    match user_input:
        case 'c':
            create_tables()
        case 'r':
            rebuild_tables()
        case 'f':
            fill_database()
        case 'p':
            print_schema()
        case 't':
            table_data()
        case 'h':
            print('\n')
        case 's':
            slow_query()
        case _:
            print("=> Invalid Input..")

    user_input = input("Your Choice: ")

print("bye!")
