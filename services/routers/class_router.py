from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from services.logic.add_class import (
    insert_single_class,
    insert_recurring_classes,
    fetch_user_classes
)
from models import Class  # your Pydantic class model

router = APIRouter()

class ClassEntry(BaseModel):
    user_id: str
    title: str
    location: str
    room: Optional[str] = None
    days: Optional[List[str]] = None
    start_time: Optional[str] = None  # ISO time string
    end_time: Optional[str] = None
    term: Optional[str] = None
    year: Optional[int] = None
    online: bool = False

@router.post("/api/classes")
def add_class(entry: ClassEntry):
    entry_dict = entry.dict()
    if entry.online:
        return insert_single_class(entry_dict)
    else:
        return insert_recurring_classes(entry_dict)

@router.get("/api/classes/{user_id}", response_model=List[Class])
def get_classes(user_id: str):
    return fetch_user_classes(user_id)
