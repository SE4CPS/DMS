import pymongo
import time

# Function to create a MongoDB connection
def create_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client

# Function to create a collection in the MongoDB database
def create_collection(client, db_name, collection_name):
    db = client[db_name]
    if collection_name in db.list_collection_names():
        db.drop_collection(collection_name)  # Drop the collection if it exists
    collection = db[collection_name]
    return collection

# Function to insert a document into the MongoDB collection
def insert_document(collection, data):
    return collection.insert_one(data)

# Function to perform queries
def perform_queries(collection, count_queries):
    total_time = 0
    for i in range(count_queries):
        make = f"Make_{i}"
        model = f"Model_{i}"
        year = 2000 + i
        data = {"_id": i, "make": make, "model": model, "year": year}

        # Measure time for inserting a record
        start_time = time.time()
        insert_document(collection, data)
        total_time += time.time() - start_time

    return total_time

# Function to add documents to the collection
def add_documents(collection, num_documents):
    for i in range(num_documents):
        make = f"Make_{i}"
        model = f"Model_{i}"
        year = 2000 + i
        data = {"_id": i, "make": make, "model": model, "year": year}
        insert_document(collection, data)

# Check for existing documents with conflicting _id values
def check_existing_documents(collection, num_documents):
    existing_ids = set(collection.distinct("_id"))
    conflicting_ids = set(range(num_documents)).intersection(existing_ids)
    if conflicting_ids:
        print(f"Found documents with conflicting _id values: {conflicting_ids}")
        # Remove documents with conflicting _id values
        collection.delete_many({"_id": {"$in": list(conflicting_ids)}})

# Main function
def main():
    client = create_connection()

    if client is not None:
        db_name = "test_database"
        collection_name = "vehicles"
        collection = create_collection(client, db_name, collection_name)
        count_documents = 100
        count_queries = 100

        # Check for existing documents with conflicting _id values
        check_existing_documents(collection, count_documents)

        # Add documents to the collection
        add_documents(collection, count_documents)

        # Perform queries
        total_time = perform_queries(collection, count_queries)
        print(f"Total Time for {count_queries} queries: {total_time} seconds")

        # Close the MongoDB connection
        client.close()
    else:
        print("Error! Unable to create MongoDB connection.")

if __name__ == '__main__':
    main()
