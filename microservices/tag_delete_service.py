import os
import time
from pymongo import MongoClient
from bson import ObjectId

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["student_calendar"]
users = db["users"]

# File paths
base_dir = os.path.dirname(__file__)
input_file = os.path.join(base_dir, "..", "shared-files", "tag-delete-request.txt")
output_file = os.path.join(base_dir, "..", "shared-files", "tag-delete-response.txt")

print("Tag Delete Microservice running...")

while True:
    if os.path.exists(input_file):
        try:
            with open(input_file, "r") as f:
                lines = f.read().strip().splitlines()

            if not lines:
                time.sleep(0.5)
                continue

            open(input_file, "w").close()

            data = {}
            for line in lines:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    data[key] = value

            required_keys = ["email", "type", "title", "tag"]
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing required field: {key}")

            user_email = data["email"]
            item_type = data["type"]  # task, class, event
            title = data["title"]
            tag_to_remove = data["tag"]
            apply_all = data.get("apply_all", "false").lower() == "true"
            date = data.get("date")  # optional

            user = users.find_one({"email": user_email})
            if not user:
                raise ValueError("User not found.")

            # Proper plural mapping
            collection_key = {
                "class": "classes",
                "event": "events",
                "task": "tasks"
            }.get(item_type)

            if not collection_key:
                raise ValueError(f"Invalid item_type: {item_type}")

            items = user.get(collection_key, [])
            print(f"Found {len(items)} {collection_key}")
            updated = False

            for item in items:
                if item.get("title") != title:
                    continue

                date_field = {
                    "class": "class_date",
                    "event": "event_date",
                    "task": "due_date"
                }[item_type]

                if not apply_all:
                    if date_field not in item or item[date_field] != date:
                        continue

                tags = set(item.get("tags", []))
                if tag_to_remove in tags:
                    tags.remove(tag_to_remove)
                    item["tags"] = list(tags)
                    updated = True
                    print(f"✅ Removed tag '{tag_to_remove}' from '{item['title']}'")

            if not updated:
                raise ValueError("No matching item with tag found for deletion.")

            users.update_one(
                {"email": user_email},
                {"$set": {collection_key: items}}
            )

            result_msg = f"Tag '{tag_to_remove}' removed from {item_type}(s)."
            print(result_msg)
            with open(output_file, "w") as f:
                f.write(result_msg)

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print("❌", error_msg)
            with open(output_file, "w") as f:
                f.write(error_msg)

    time.sleep(0.5)
