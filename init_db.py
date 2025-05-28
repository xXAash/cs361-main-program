from datetime import datetime, date, time, timezone
from passlib.hash import bcrypt
from bson import ObjectId
from db import db

# Ensure email uniqueness
db.users.create_index("email", unique=True)

# Sample user (with embedded data)
user_id = ObjectId()

user_doc = {
    "_id": user_id,
    "email": "testuser@example.com",
    "password": bcrypt.hash("test1234"),
    "created_at": datetime.now(timezone.utc),
    "classes": [
        {
            "_id": ObjectId(),
            "title": "CS340 - Database Systems",
            "location": "Kidder Hall",
            "room": "364",
            "class_date": date(2025, 5, 26).isoformat(),
            "start_time": time(8, 0).isoformat(),
            "end_time": time(9, 50).isoformat()
        },
        {
            "_id": ObjectId(),
            "title": "CS340 - Database Systems",
            "location": "Kidder Hall",
            "room": "364",
            "class_date": date(2025, 5, 28).isoformat(),
            "start_time": time(8, 0).isoformat(),
            "end_time": time(9, 50).isoformat()
        },
        {
            "_id": ObjectId(),
            "title": "CS340 - Database Systems",
            "location": "Kidder Hall",
            "room": "364",
            "class_date": date(2025, 6, 2).isoformat(),
            "start_time": time(8, 0).isoformat(),
            "end_time": time(9, 50).isoformat()
        },
        {
            "_id": ObjectId(),
            "title": "CS340 - Database Systems",
            "location": "Kidder Hall",
            "room": "364",
            "class_date": date(2025, 2, 4).isoformat(),
            "start_time": time(8, 0).isoformat(),
            "end_time": time(9, 50).isoformat()
        },
        {
            "_id": ObjectId(),
            "title": "CS361 - Software Engineering I",
            "online": True,
            "location": "(URL to online class)"
        }
    ],
    "events": [
        {
            "_id": ObjectId(),
            "title": "Code Demo",
            "location": "Online",
            "date": date(2025, 5, 27).isoformat(),
            "start_time": time(9, 40).isoformat(),
            "end_time": time(9, 50).isoformat()
        }
    ],
    "tasks": [
        {
            "_id": ObjectId(),
            "title": "Assignment 3",
            "description": "Add persistent storage to calendar app",
            "due_date": date(2025, 5, 29).isoformat(),
            "due_time": time(23, 59).isoformat(),
            "linked_to": {
                "type": "class",
                "title": "CS340 - Database Systems"
            }
        }
    ]
}

db.users.insert_one(user_doc)

print("MongoDB collections initialized with sample data.")