from pymongo import MongoClient
from pymongo import GEOSPHERE

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Assuming MongoDB is running locally on the default port

# Access the "geospatial" database
db = client['geospatial']

# Create a collection named "locations" with a 2dsphere index for geospatial queries
db.locations.create_index([("location", GEOSPHERE)])

# Insert a document with geospatial data
location_data = {
    "name": "Central Park",
    "location": {"type": "Point", "coordinates": [40.785091, -73.968285]}
}
db.locations.insert_one(location_data)

# Find locations near a specific point (e.g., Central Park)
query = {
    "location": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": [40.785091, -73.968285]  # Coordinates of Central Park
            },
            "$maxDistance": 2000  # Maximum distance in meters (adjust as needed)
        }
    }
}
nearby_locations = db.locations.find(query)
print("Locations near Central Park:")
for location in nearby_locations:
    print(location)

# Close the connection to MongoDB
client.close()