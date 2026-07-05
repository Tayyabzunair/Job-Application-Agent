"""Quick test to check MongoDB Atlas connection."""
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")

if not uri:
    print("MONGODB_URI not found in .env file!")
    exit()

print("Connecting to MongoDB Atlas...")

try:
    client = MongoClient(uri)
    # 'ping' is the simplest command to verify the connection works
    client.admin.command("ping")
    print("Connected successfully!")

    # Show available databases (proves we can talk to the server)
    print("Databases:", client.list_database_names())

except Exception as e:
    print(f"Connection failed: {e}")
