# microservices/add_tag_router.py

from fastapi import APIRouter
from pydantic import BaseModel
import os

router = APIRouter()

class TagAddRequest(BaseModel):
    content: str

@router.post("/write-tag-add")
async def write_tag_add(req: TagAddRequest):
    path = os.path.join("shared-files", "tag-add-request.txt")
    with open(path, "w") as f:
        f.write(req.content)
    return {"status": "ok"}

@router.get("/read-tag-add-response")
def read_tag_add_response():
    path = os.path.join("shared-files", "tag-add-response.txt")
    if not os.path.exists(path):
        return ""
    with open(path, "r") as f:
        return f.read()

@router.post("/clear-tag-add-response")
def clear_tag_add_response():
    path = os.path.join("shared-files", "tag-add-response.txt")
    with open(path, "w") as f:
        f.write("")
    return {"status": "cleared"}
