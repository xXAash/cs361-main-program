from fastapi import HTTPException
from bson import ObjectId
from db import db
from services.utils.objectID_converter import convert_objectid_to_string

def insert_event(event_data: dict, user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    event_data["_id"] = ObjectId()
    if "event_date" in event_data:
        event_data["event_date"] = event_data["event_date"].isoformat()
    if "start_time" in event_data:
        event_data["start_time"] = event_data["start_time"].isoformat()
    if "end_time" in event_data:
        event_data["end_time"] = event_data["end_time"].isoformat()

    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"events": event_data}}
    )
    return {"msg": "Event added successfully"}

def insert_recurring_events(events: list[dict], user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for e in events:
        e["_id"] = ObjectId()
        if "event_date" in e:
            e["event_date"] = e["event_date"].isoformat()
        if "start_time" in e:
            e["start_time"] = e["start_time"].isoformat()
        if "end_time" in e:
            e["end_time"] = e["end_time"].isoformat()

    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"events": {"$each": events}}}
    )
    return {"msg": f"{len(events)} recurring events added"}

def fetch_user_events(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    events = user.get("events", [])
    
    # ✅ Remove user_id from each event before returning
    for event in events:
        event.pop("user_id", None)

    return convert_objectid_to_string(events)