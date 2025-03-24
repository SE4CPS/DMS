**Team3:** <br>
Han Nguyen <br>
Raymond Lee <br>
Junah Kim <br>

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
    

/static:<br>
    style.css              # Styles the index.html, styles the frontend
/templates:<br>
    index.html <br>        # The frontend
/backend: 
    crud.py       
    
## How to Run

1. Make sure that PostgreSQL is installed. To install PostgreSQL on MacOS using Brew, use: `brew install postgresql` on MacOS. 
2. Create a virtual environment using `python3 -m venv venv`.
3. Activate the virtual environment using `source venv/bin/activate` if you are on Mac.
4. Once the virtual environment is running, install the requirements needed for the project: `pip install -r requirements.txt`.
5. Create a config file to store the database API key in the team3 directory using `touch .env`. Then insert the database API key like so `database_url=[insert database api key here]`.
6. Run the app using: `python3 app.py`.
7. Navigate to the local host link to see the webapp in the browser: `http://127.0.0.1:5000`. 
8. Add endpoints to the URL as needed for testing e.g (`http://127.0.0.1:5000/flowers`).

## Note for Developers

1. To add additional requirements to the requirements.txt file, do `python3 -m pip freeze > requirements.txt`.
