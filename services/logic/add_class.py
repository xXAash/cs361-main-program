from fastapi import HTTPException
from bson import ObjectId
from datetime import time
from db import db
from services.utils.recurring_generator import generate_recurring_items
from services.utils.objectID_converter import convert_objectid_to_string

def insert_single_class(entry: dict):
    user = db.users.find_one({"_id": ObjectId(entry["user_id"])})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    class_instance = {
        "_id": ObjectId(),
        "title": entry["title"],
        "location": entry["location"],
        "room": entry.get("room"),
        "online": True,
        "class_date": None,
        "start_time": None,
        "end_time": None
    }

    db.users.update_one(
        {"_id": ObjectId(entry["user_id"])},
        {"$push": {"classes": class_instance}}
    )

    return {"msg": "Online class added"}

def insert_recurring_classes(entry: dict):
    user = db.users.find_one({"_id": ObjectId(entry["user_id"])})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get list of class dates using your term generator
    from services.utils.term_dates_generator import generate_term_dates
    start_date, end_date = generate_term_dates(entry["term"], entry["year"])

    # Parse time strings into time objects
    start_time = entry["start_time"]
    end_time = entry["end_time"]

    generated_classes = generate_recurring_items(
        title=entry["title"],
        location=entry["location"],
        start_time=start_time,
        end_time=end_time,
        days=entry["days"],
        start_date=start_date,
        end_date=end_date,
        item_type="class",
        extras={"room": entry["room"], "online": False}
    )

    for c in generated_classes:
        c["_id"] = ObjectId()
        if c.get("class_date") and hasattr(c["class_date"], "isoformat"):
            c["class_date"] = c["class_date"].isoformat()

    db.users.update_one(
        {"_id": ObjectId(entry["user_id"])},
        {"$push": {"classes": {"$each": generated_classes}}}
    )

    return {"msg": f"{len(generated_classes)} class instances added"}

def fetch_user_classes(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    classes = user.get("classes", [])

    # ✅ Strip user_id before returning to avoid response validation error
    for cls in classes:
        cls.pop("user_id", None)

    return convert_objectid_to_string(classes)