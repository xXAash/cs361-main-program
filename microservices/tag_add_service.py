import os
import time
from pymongo import MongoClient
from bson import ObjectId, errors

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["student_calendar"]
users = db["users"]

# File paths
base_dir = os.path.dirname(__file__)
input_file = os.path.join(base_dir, "..", "shared-files", "tag-add-request.txt")
output_file = os.path.join(base_dir, "..", "shared-files", "tag-add-response.txt")

print("Tag Add Microservice running...")

while True:
    if os.path.exists(input_file):
        try:
            with open(input_file, "r") as f:
                lines = f.read().strip().splitlines()

            # Skip empty files
            if not lines:
                time.sleep(0.5)
                continue

            print("\n=== File Read ===")
            print(lines)

            # Clear file after reading
            open(input_file, "w").close()

            # Build dictionary safely
            data = {}
            for line in lines:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    data[key] = value

            print("=== Parsed Data ===")
            print(data)

            # Confirm required fields
            required_keys = ["email", "type", "title", "tags"]
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing required field: '{key}'. Keys found: {list(data.keys())}")

            user_email = data["email"]
            item_type = data["type"]
            target_title = data["title"]
            new_tags = [tag.strip() for tag in data["tags"].split(",")]
            apply_all = data.get("apply_all", "false").lower() == "true"
            target_date = data.get("date")  # optional

            print(f"Looking up user: {user_email}")
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
                title_matches = item.get("title") == target_title
                date_matches = True  # default true if no date specified

                if not apply_all and target_date:
                    if item_type == "class":
                        date_matches = item.get("class_date") == target_date
                    elif item_type == "event":
                        date_matches = item.get("event_date") == target_date
                    elif item_type == "task":
                        date_matches = item.get("due_date") == target_date

                if (apply_all and title_matches) or (not apply_all and title_matches and date_matches):
                    existing = set(item.get("tags", []))
                    item["tags"] = list(existing.union(new_tags))
                    updated = True
                    print(f"✅ Tags added to item: {item.get('title')}")

            if not updated:
                raise ValueError("Matching item not found for tag addition.")

            # Save changes to DB
            users.update_one(
                {"email": user_email},
                {"$set": {collection_key: items}}
            )

            result_msg = f"Tags {new_tags} added to {item_type}(s)."
            print(result_msg)
            with open(output_file, "w") as f:
                f.write(result_msg)

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print("❌", error_msg)
            with open(output_file, "w") as f:
                f.write(error_msg)

    time.sleep(0.5)
