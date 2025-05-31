from pydantic import BaseModel
from typing import List, Optional
from datetime import time
from models import Task, Event, Class

class AddTaskRequest(BaseModel):
    user_id: str
    new_task: Task

class AddEventRequest(BaseModel):
    user_id: str
    new_event: Event

class AddClassRequest(BaseModel):
    user_id: str
    new_class: Class

class AddRecurringClassRequest(BaseModel):
    user_id: str
    title: str
    location: str
    room: Optional[str] = None
    start_time: time
    end_time: time
    days: List[str]
    term: str
    year: int