from fastapi import APIRouter
from typing import List
from services.logic.add_task import create_task, fetch_user_tasks
from services.logic.add_requests import AddTaskRequest  # request wrapper
from models import Task

router = APIRouter()

@router.post("/api/tasks")
def post_task(req: AddTaskRequest):  # use wrapper
    return create_task(req)

@router.get("/api/tasks/{user_id}", response_model=List[Task])
def get_tasks(user_id: str):
    return fetch_user_tasks(user_id)

@router.post("/api/tasks")
def post_task(req: AddTaskRequest):
    print("🛠 Received request body:", req.dict())
    return create_task(req)