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
.env                        # Store db_url

/database:
    db_connection.py        # Connect to database
    db_init.py              # Initialize database schema
    
    crud.py                 # Handle CRUD operations for flower table
    ping.py                 # Check database route health
    print.py                # Formats flower data for frontend

/frontend:

/backend: 
