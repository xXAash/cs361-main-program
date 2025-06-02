from fastapi import APIRouter
from typing import List
from models import Event
from services.logic.add_event import (
    insert_single_event,
    insert_recurring_events,
    fetch_user_events
)
from services.logic.add_requests import AddEventRequest, AddRecurringEventRequest

router = APIRouter()

@router.post("/api/events")
def add_event(req: AddEventRequest):
    return insert_single_event(req)

@router.post("/api/events/recurring")
def add_recurring_event(req: AddRecurringEventRequest):
    return insert_recurring_events(req)

@router.get("/api/events/{user_id}", response_model=List[Event])
def get_events(user_id: str):
    return fetch_user_events(user_id)
