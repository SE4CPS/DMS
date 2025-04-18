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
.env                        # Store db_url, remember to delete pooler for it to work. <br>

app.py                      # Routing command to interact with database & will be connected with frontend. <br>

/database:<br>
    db_connection.py        # Connect to database <br>
    db_init.py              # Initialize database schema <br>
    

/frontend:
    index.html              # Sample Interfaces for backend testing -- Not the main interfaces.  <br>  
/backend: 
    crud.py                 # In progress <br>
    # Insert data into table
    
## How to Run

0. Make sure that PostgreSQL is installed. To install PostgreSQL on MacOS using Brew, use: `brew install postgresql` on MacOS. 
1. Create a virtual environment using `python3 -m venv venv`.
2. Activate the virtual environment using `source venv/bin/activate` if you are on Mac.
3. Once the virtual environment is running, install the requirements needed for the project: `pip install -r requirements.txt`.
4. Run the app using: `python3 app.py`.
5. Navigate to the local host link to see the webapp in the browser: `http://127.0.0.1:5000`. 
6. Add endpoints to the URL as needed for testing e.g (`http://127.0.0.1:5000/flowers`).

## Note for Developers

1. To add additional requirements to the requirements.txt file, do `python3 -m pip freeze > requirements.txt`.