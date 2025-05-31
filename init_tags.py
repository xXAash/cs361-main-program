from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["student_calendar"]
users = db["users"]

# Update each user's data
for user in users.find():
    updated = False

    # Fix classes
    new_classes = []
    for cls in user.get("classes", []):
        if "tags" not in cls:
            cls["tags"] = []
            updated = True
        new_classes.append(cls)

    # Fix events
    new_events = []
    for evt in user.get("events", []):
        if "tags" not in evt:
            evt["tags"] = []
            updated = True
        new_events.append(evt)

    # Fix tasks
    new_tasks = []
    for task in user.get("tasks", []):
        if "tags" not in task:
            task["tags"] = []
            updated = True
        new_tasks.append(task)

    # Apply updates
    if updated:
        users.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "classes": new_classes,
                "events": new_events,
                "tasks": new_tasks
            }}
        )
        print(f"Updated user: {user['email']}")
