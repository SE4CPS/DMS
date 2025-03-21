team3:
Han Nguyen
Raymond Lee
Junah Kim

# Flower Water Tracking System
Web application to track flower watering status, indicate when the flower will to be watered again.

## Technologies:
Database: PostgreSQL, Neon database <br> 
Frontend: HTML/CSS <br>
Backend: Python - Flask framework <br>

## Features:
- Track flower watering status.
- View when flower need watering.
- Add, update, and delete flower records. 
- Simple web interfaces.

## Project stucture:
.gitignore  
.env                        # Store db_url, remember to delete pooler for it to work.

/database:<br>
    db_connection.py        # Connect to database <br>
    db_init.py              # Initialize database schema <br>
    

/frontend:

/backend: 
    crud.py                 # In progress <br>
    # Insert data into table
