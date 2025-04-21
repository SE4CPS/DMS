# Flower Water Tracking System

**Team Members:**
- Han Nguyen
- Raymond Lee
- Junah Kim

A web application to track flower watering status and indicate when flowers need to be watered again.

## Technologies

### Backend
- Framework: Python Flask 3.1.0
- Database: Neon (Serverless PostgreSQL)

### Frontend
- HTML/CSS

### Dependencies
- python-dotenv 1.0.1
- psycopg2-binary 2.9.10
- Faker 37.1.0

## Features

- Track flower watering status and water levels
- View flowers that need watering
- Add, update, and delete flower records
- Automatic water level updates
- Performance comparison between query implementations
- Simple web interface

## Project Structure

```
.
├── .gitignore                    # Git ignore file.
├── .env                          # API key.
├── app.py                        # Main Flask application with all routes.
├── requirements.txt              # Project dependencies.
├── database/
│   ├── db_connection.py          # Database connection management.
│   └── db_init.py                # Database schema initialization.
│   └── generate_data.py          # Insert data in the database & ensure encrypted table have same data as normal table.
├── static/
│   └── style.css                 # CSS styles for the frontend.
├── templates/
│   └── index.html                # Main frontend template.           
└── backend/
    └── test_insert_data          # Test insertion         
    └── test_queries              # Test querying    
```

## Available Endpoints:
- `GET /` - Home page
- `GET /flowers` - Get all flowers
- `GET /flowers/needs_watering` - Get flowers that need watering
- `PUT /flowers/water/<id>` - Update water level for a specific flower
- `POST /flowers` - Add a new flower
- `PUT /flowers/<id>` - Update flower information
- `GET /updated_flowers_level/` - Get updated water levels
- `GET /slow-query` - Performance test endpoint (slow implementation)
- `GET /fast-query` - Performance test endpoint (optimized implementation)

## Installation and Setup
## How to Run

1. **Create a virtual environment** 
   **Activate virtual environment**
  

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   - Create a Neon database account at [https://neon.tech](https://neon.tech)
   - Create a new project and get your connection string
   - Create a `.env` file in the project root:
     ```
     DATABASE_URL=your_neon_connection_string
     ```
   - Note: Remove the `?sslmode=require` from the connection string if present

4. **Run the Application**
   ```bash
   python3 app.py
   ```

5. **Access the Application**
   - Open your browser and navigate to `http://127.0.0.1:5000`
   - Use the available endpoints as needed

## Development Notes

1. **Updating Requirements**
   ```bash
   pip freeze > requirements.txt
   ```

2. **Database Initialization**
   - The database schema is automatically initialized when the application starts

3. **Performance Testing**
   - Endpoints available at `/slow-query` and `/fast-query` for comparison