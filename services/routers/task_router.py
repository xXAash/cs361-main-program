from fastapi import APIRouter
from typing import List
from services.logic.add_task import create_task, fetch_user_tasks
from models import Task

router = APIRouter()

@router.post("/api/tasks")
def post_task(task: Task):
    return create_task(task)

@router.get("/api/tasks/{user_id}", response_model=List[Task])
def get_tasks(user_id: str):
    return fetch_user_tasks(user_id)
