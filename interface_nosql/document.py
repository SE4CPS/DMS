from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Access the "bike" database
db = client['bike']

# Access the "bike_collection" collection (if it doesn't exist, MongoDB will create it)
collection = db['bike_collection']

# Insert a document into the collection
bike_data = {
    "brand": "Trek",
    "model": "FX 2 Disc",
    "year": 2021,
    "color": "Black",
    "price": 800
}
result = collection.insert_one(bike_data)
print("Inserted document ID:", result.inserted_id)

# Find a document in the collection
query = {"brand": "Trek"}
bike = collection.find_one(query)
print("Found bike:", bike)

# Update a document in the collection
update_query = {"brand": "Trek"}
new_values = {"$set": {"price": 750}}
collection.update_one(update_query, new_values)
print("Updated bike price")

# Find all documents in the collection
all_bikes = collection.find()
print("All bikes in the collection:")
for bike in all_bikes:
    print(bike)

# Delete a document from the collection
#delete_query = {"brand": "Trek"}
#collection.delete_one(delete_query)
#print("Deleted bike")

# Drop the entire collection (use with caution)
# collection.drop()

# Close the connection to MongoDB
client.close()