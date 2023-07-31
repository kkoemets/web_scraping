import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Create a client
# define client with port number from os.env
client = MongoClient(f'mongodb://localhost:{os.getenv("MONGO_PORT", "27017")}/')

# Access the database
db = client["mydatabase"]

# Access the collection
collection = db["listingdetails"]

# Find documents with a specific href
href = 'http://xyz.com'
documents = collection.find({"href": href})

# Print out the documents
for document in documents:
    print(document)
