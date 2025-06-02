from fastapi import HTTPException
from bson import ObjectId
from datetime import time
from db import db
from services.utils.objectID_converter import convert_objectid_to_string
from services.utils.recurring_generator import generate_recurring_items
from services.logic.add_requests import AddEventRequest, AddRecurringEventRequest

def insert_single_event(req: AddEventRequest):
    user = db.users.find_one({"_id": ObjectId(req.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_event = req.new_event.dict()
    new_event["_id"] = ObjectId()
    new_event["tags"] = []

    if "event_date" in new_event:
        new_event["event_date"] = new_event["event_date"].isoformat()
    if "start_time" in new_event:
        new_event["start_time"] = new_event["start_time"].isoformat()
    if "end_time" in new_event:
        new_event["end_time"] = new_event["end_time"].isoformat()

    db.users.update_one(
        {"_id": ObjectId(req.user_id)},
        {"$push": {"events": new_event}}
    )

    return {"msg": "Event added successfully"}

def insert_recurring_events(req: AddRecurringEventRequest):
    user = db.users.find_one({"_id": ObjectId(req.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    generated_events = generate_recurring_items(
        title=req.title,
        location=req.location,
        start_time=req.start_time,
        end_time=req.end_time,
        days=req.days,
        start_date=req.start_date,
        end_date=req.end_date,
        item_type="event",
        extras={}
    )

    for event in generated_events:
        event["_id"] = ObjectId()
        event["tags"] = []
        if "event_date" in event:
            event["event_date"] = event["event_date"].isoformat()
        if "start_time" in event and isinstance(event["start_time"], time):
            event["start_time"] = event["start_time"].isoformat()
        if "end_time" in event and isinstance(event["end_time"], time):
            event["end_time"] = event["end_time"].isoformat()

    db.users.update_one(
        {"_id": ObjectId(req.user_id)},
        {"$push": {"events": {"$each": generated_events}}}
    )

    return {"msg": f"{len(generated_events)} event instances added"}

def fetch_user_events(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return convert_objectid_to_string(user.get("events", []))
