# microservices/tag_delete_router.py

from fastapi import APIRouter
from pydantic import BaseModel
import os

router = APIRouter()

class TagDeleteRequest(BaseModel):
    content: str

@router.post("/write-tag-delete")
async def write_tag_delete(req: TagDeleteRequest):
    path = os.path.join("shared-files", "tag-delete-request.txt")
    with open(path, "w") as f:
        f.write(req.content)
    return {"status": "ok"}

@router.get("/read-tag-delete-response")
def read_tag_delete_response():
    path = os.path.join("shared-files", "tag-delete-response.txt")
    if not os.path.exists(path):
        return ""
    with open(path, "r") as f:
        return f.read()

@router.post("/clear-tag-delete-response")
def clear_tag_delete_response():
    path = os.path.join("shared-files", "tag-delete-response.txt")
    with open(path, "w") as f:
        f.write("")
    return {"status": "cleared"}
