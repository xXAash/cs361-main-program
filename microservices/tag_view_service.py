import os
import time
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["student_calendar"]
users = db["users"]

# File paths for microservice communication (optional if using microservices with txt files)
base_dir = os.path.dirname(__file__)
input_file = os.path.join(base_dir, "..", "shared-files", "tag-view-request.txt")
output_file = os.path.join(base_dir, "..", "shared-files", "tag-view-response.txt")

print("Tag View Microservice running...")

def convert_objectids(obj):
    if isinstance(obj, list):
        return [convert_objectids(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_objectids(v) for k, v in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

while True:
    if os.path.exists(input_file):
        try:
            with open(input_file, "r") as f:
                lines = f.read().strip().splitlines()

            if not lines:
                time.sleep(0.5)
                continue

            # Clear file after reading
            open(input_file, "w").close()

            data = {}
            for line in lines:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    data[key] = value

            user_id_str = data.get("email")  # rename key to 'user_id' if you want clarity
            requested_tags = data.get("tags", "")
            requested_tags = [tag.strip() for tag in requested_tags.split(",") if tag.strip()]

            if not user_id_str:
                raise ValueError("Missing user ID")

            try:
                user_obj_id = ObjectId(user_id_str)
            except InvalidId:
                raise ValueError("Invalid user ID format")

            user = users.find_one({"_id": user_obj_id})
            if not user:
                raise ValueError("User not found")

            # Collect all unique tags from user's classes, events, tasks
            all_tags_set = set()
            for collection_name in ["classes", "events", "tasks"]:
                for item in user.get(collection_name, []):
                    all_tags_set.update(item.get("tags", []))

            # If no tags requested, return empty results
            if not requested_tags:
                result = {"tags": list(all_tags_set), "classes": [], "events": [], "tasks": []}
            else:
                # Filter classes/events/tasks by matching ANY of the requested tags
                def matches_tags(item):
                    return any(tag in item.get("tags", []) for tag in requested_tags)

                filtered_classes = [c for c in user.get("classes", []) if matches_tags(c)]
                filtered_events = [e for e in user.get("events", []) if matches_tags(e)]
                filtered_tasks = [t for t in user.get("tasks", []) if matches_tags(t)]

                result = {
                    "tags": list(all_tags_set),
                    "classes": filtered_classes,
                    "events": filtered_events,
                    "tasks": filtered_tasks,
                }

                result = convert_objectids(result)

            with open(output_file, "w") as f:
                import json
                f.write(json.dumps(result))

        except Exception as e:
            err_msg = f"Error: {str(e)}"
            print(err_msg)
            with open(output_file, "w") as f:
                f.write(err_msg)

    time.sleep(0.5)