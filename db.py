from pymongo import MongoClient

# Connect to the local MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Select the project database
db = client["student_calendar"]