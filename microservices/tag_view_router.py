from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from db import db
import os

router = APIRouter()

class TagViewRequest(BaseModel):
    tags: list[str]
    
base_dir = os.path.dirname(__file__)
response_path = os.path.join(base_dir, "..", "shared-files", "tag-view-response.txt")

@router.get("/api/tags/{user_id}")
def get_all_tags(user_id: str):
    try:
        obj_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = db.users.find_one({"_id": obj_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    all_tags = set()
    for collection in ["classes", "events", "tasks"]:
        for item in user.get(collection, []):
            all_tags.update(item.get("tags", []))

    return sorted(list(all_tags))

@router.post("/api/view-tags/{user_id}")
def view_tags(user_id: str, req: TagViewRequest):
    # Read from microservice output file and return filtered data
    # Or communicate with microservice via shared file mechanism as you did for other microservices
    base_dir = os.path.dirname(__file__)
    output_file = os.path.join(base_dir, "..", "shared-files", "tag-view-response.txt")

    # Wait for the microservice to process request, or you can directly query DB here
    import time, json
    # Write the request for microservice
    input_file = os.path.join(base_dir, "..", "shared-files", "tag-view-request.txt")
    with open(input_file, "w") as f:
        content = f"email={user_id}\ntags={','.join(req.tags)}"
        f.write(content)

    # Wait for response file to be filled (simplified: wait up to 10 seconds)
    for _ in range(10):
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                data = f.read()
                if data.strip():
                    try:
                        return json.loads(data)
                    except Exception:
                        return {"error": "Invalid response format"}
        time.sleep(1)

    return {"error": "Timeout waiting for response from tag view microservice"}

@router.get("/read-tag-view-response")
def read_tag_view_response():
    if not os.path.exists(response_path):
        return ""
    with open(response_path, "r") as f:
        return f.read()

@router.post("/clear-tag-view-response")
def clear_tag_view_response():
    with open(response_path, "w") as f:
        f.write("")
    return {"status": "cleared"}