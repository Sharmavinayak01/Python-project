from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")

client = MongoClient(uri)

# MongoDB connection test
client.admin.command("ping")

print("MongoDB connected successfully!")

db = client["ai_chatbot"]

print("Database selected: ai_chatbot")