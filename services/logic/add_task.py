from fastapi import HTTPException
from bson import ObjectId
from db import db
from models import Task
from services.utils.objectID_converter import convert_objectid_to_string

def create_task(task: Task):
    user = db.users.find_one({"_id": ObjectId(task.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if task.linked_to:
        valid_titles = []
        if task.linked_to.type == "class":
            valid_titles = [c["title"] for c in user["classes"]]
        elif task.linked_to.type == "event":
            valid_titles = [e["title"] for e in user["events"]]

        if task.linked_to.title not in valid_titles:
            raise HTTPException(status_code=400, detail="Linked title not found")

    task_dict = task.dict(exclude={"user_id"})
    task_dict["_id"] = ObjectId()

    task_dict["due_date"] = task.due_date.isoformat()
    task_dict["due_time"] = task.due_time.isoformat()

    db.users.update_one(
        {"_id": ObjectId(task.user_id)},
        {"$push": {"tasks": task_dict}}
    )
    return {"msg": "Task added successfully"}

def fetch_user_tasks(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    tasks = user.get("tasks", [])
    # Strip user_id from each task before returning
    for task in tasks:
        task.pop("user_id", None)
    return convert_objectid_to_string(tasks)

