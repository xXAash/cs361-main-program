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

            # Confirm expected fields
            required_keys = ["email", "type", "item_id", "tags"]
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing required field: '{key}'. Keys found: {list(data.keys())}")

            user_email = data["email"]
            item_type = data["type"]  # task, class, or event
            item_id = data["item_id"]
            new_tags = [tag.strip() for tag in data["tags"].split(",")]
            apply_all = data.get("apply_all", "false").lower() == "true"
            target_title = data.get("title", "")

            print(f"Looking up user: {user_email}")
            user = users.find_one({"email": user_email})
            if not user:
                raise ValueError("User not found.")

            updated = False
            items = user.get(f"{item_type}s", [])
            print(f"Found {len(items)} {item_type}s")

            for item in items:
                try:
                    match = ObjectId(item_id) == item.get("_id")
                except errors.InvalidId:
                    match = False

                if (apply_all and item.get("title") == target_title) or match:
                    existing = set(item.get("tags", []))
                    item["tags"] = list(existing.union(new_tags))
                    updated = True
                    print(f"✅ Tags added to item: {item.get('title')}")

            if not updated:
                raise ValueError("Matching item not found for tag addition.")

            # Write back updated array
            users.update_one(
                {"email": user_email},
                {"$set": {f"{item_type}s": items}}
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
