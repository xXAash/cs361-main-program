from fastapi import APIRouter
from typing import List
from services.logic.add_class import (
    insert_single_class,
    insert_recurring_classes,
    fetch_user_classes
)
from services.logic.add_requests import AddClassRequest, AddRecurringClassRequest
from models import Class

router = APIRouter()

@router.post("/api/classes")
def add_class(req: AddClassRequest):
    return insert_single_class(req)

@router.post("/api/classes/recurring")
def add_recurring_class(req: AddRecurringClassRequest):
    return insert_recurring_classes(req)

@router.get("/api/classes/{user_id}", response_model=List[Class])
def get_classes(user_id: str):
    return fetch_user_classes(user_id)
