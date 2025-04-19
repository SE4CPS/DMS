import psycopg2

# get postgresql url
print("   | Database Url: postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require")
DB_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

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
        print("  | Result:")
        print(cur)
    except Exception as e:
        print("   | SQL EXECUTE ERROR: ", e)

def create_tables():
    execute(
    """
    CREATE TABLE team10_flowers (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        last_watered DATE NOT NULL,
        water_level INT NOT NULL,
        min_water_required INT NOT NULL
    );
    CREATE TABLE team10_customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
    );
    CREATE TABLE team10_orders (
        id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES team10_customers(id),
        flower_id INT REFERENCES team10_flowers(id),
        order_date DATE
    );
    """
    )
def rebuild_tables():
    execute(
    """
    """
    )
def fill_database():
    execute(
    """
    """
    )
def print_schema():
    execute(
    """
    """
    )

def print_prompt():
    print("|----------------------------------|")
    print("| Admin Tool                       |")
    print("|----------------------------------|")
    print("| Options:                         |")
    print("|----------------------------------|")
    print("| c -> Create Tables in Postgresql |")
    print("| r -> Rebuild Tables              |")
    print("| f -> Fill Database with Data     |")
    print("| p -> Print Schema of Table       |")
    print("| h -> Print this prompt           |")
    print("|----------------------------------|")

user_input = 'a'
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
        case _:
            print("=> Invalid Input..")

    user_input = input("Your Choice: ")

print("bye!")
