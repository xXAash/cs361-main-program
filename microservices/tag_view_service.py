import os
import time
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["student_calendar"]
users = db["users"]

# File paths
base_dir = os.path.dirname(__file__)
input_file = os.path.join(base_dir, "..", "shared-files", "tag-view-request.txt")
output_file = os.path.join(base_dir, "..", "shared-files", "tag-view-response.txt")

print("Tag View Microservice running...")

while True:
    if os.path.exists(input_file):
        try:
            with open(input_file, "r") as f:
                lines = f.read().strip().splitlines()

            if not lines:
                time.sleep(0.5)
                continue

            print("\n=== File Read ===")
            print(lines)

            open(input_file, "w").close()

            data = {}
            for line in lines:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    data[key] = value

            print("=== Parsed Data ===")
            print(data)

            email = data["email"]
            tag_filter = set(tag.strip() for tag in data["tags"].split(","))
            type_filter = data.get("type", "all").lower()

            user = users.find_one({"email": email})
            if not user:
                raise ValueError("User not found.")

            output_lines = []

            def check_and_add(item_list, label):
                for item in item_list:
                    item_tags = set(item.get("tags", []))
                    if tag_filter.intersection(item_tags):
                        title = item.get("title", "[No Title]")
                        output_lines.append(f"[{label}] {title} – Tags: {', '.join(item_tags)}")

            if type_filter in ("task", "all"):
                check_and_add(user.get("tasks", []), "Task")

            if type_filter in ("class", "all"):
                check_and_add(user.get("classes", []), "Class")

            if type_filter in ("event", "all"):
                check_and_add(user.get("events", []), "Event")

            if not output_lines:
                output_lines.append("No matching items found.")

            with open(output_file, "w") as f:
                f.write("\n".join(output_lines))

            print("✅ Tag View Response Written")

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print("❌", error_msg)
            with open(output_file, "w") as f:
                f.write(error_msg)

    time.sleep(0.5)
