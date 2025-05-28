from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.logic.add_event import (
    insert_event, 
    insert_recurring_events, 
    fetch_user_events
)
from models import Event
from services.utils.recurring_generator import generate_recurring_items

router = APIRouter()

@router.post("/api/events")
def add_event(entry: Event):
    if entry.recurring and entry.recurring.is_recurring:
        generated = generate_recurring_items(
        title=entry.title,
        location=entry.location,
        start_time=entry.start_time,
        end_time=entry.end_time,
        days=entry.recurring.days,
        start_date=entry.recurring.start_date,
        end_date=entry.recurring.end_date,
        item_type="event",
        extras={"user_id": entry.user_id}
    )
        return insert_recurring_events(generated, entry.user_id)
    else:
        return insert_event(entry.dict(), entry.user_id)

@router.get("/api/events/{user_id}")
def get_events(user_id: str):
    events = fetch_user_events(user_id)
    return JSONResponse(content=events)