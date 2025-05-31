from fastapi import HTTPException
from bson import ObjectId
from db import db
from services.utils.term_dates_generator import generate_term_dates
from services.utils.recurring_generator import generate_recurring_items
from services.utils.objectID_converter import convert_objectid_to_string
from services.logic.add_requests import AddClassRequest, AddRecurringClassRequest
from datetime import time

def insert_single_class(req: AddClassRequest):
    user = db.users.find_one({"_id": ObjectId(req.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_class = req.new_class.dict()
    new_class["_id"] = ObjectId()
    new_class["class_date"] = new_class.get("class_date")
    new_class["start_time"] = new_class.get("start_time")
    new_class["end_time"] = new_class.get("end_time")

    db.users.update_one(
        {"_id": ObjectId(req.user_id)},
        {"$push": {"classes": new_class}}
    )

    return {"msg": "Class added"}

def insert_recurring_classes(req: AddRecurringClassRequest):
    user = db.users.find_one({"_id": ObjectId(req.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    start_date, end_date = generate_term_dates(req.term, req.year)

    generated_classes = generate_recurring_items(
        title=req.title,
        location=req.location,
        start_time=req.start_time,
        end_time=req.end_time,
        days=req.days,
        start_date=start_date,
        end_date=end_date,
        item_type="class",
        extras={"room": req.room, "online": False}
    )

    for cls in generated_classes:
        cls["_id"] = ObjectId()
        if "class_date" in cls:
            cls["class_date"] = cls["class_date"].isoformat()

    db.users.update_one(
        {"_id": ObjectId(req.user_id)},
        {"$push": {"classes": {"$each": generated_classes}}}
    )

    return {"msg": f"{len(generated_classes)} class instances added"}

def fetch_user_classes(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    classes = user.get("classes", [])
    for cls in classes:
        cls.pop("user_id", None)

    return convert_objectid_to_string(classes)
