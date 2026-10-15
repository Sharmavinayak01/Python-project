from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))

# Database
db = client["ai_chatbot"]

# Collection
messages = db["messages"]

# Test message
messages.insert_one({
    "role": "user",
    "content": "MongoDB connection test",
    "created_at": datetime.utcnow()
})

print("Message inserted successfully!")