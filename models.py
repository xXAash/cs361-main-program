from typing import List, Optional, Literal
from datetime import date, time
from pydantic import BaseModel

# Used to link a task to a class or event by ObjectId string
class LinkedReference(BaseModel):
    type: Literal["class", "event"]
    title: str  # Title of the class or event being linked

# Recurrence configuration for events or classes
class RecurringConfig(BaseModel):
    is_recurring: bool
    days: Optional[List[str]] = None         # e.g. ["Monday", "Wednesday"]
    start_date: Optional[date] = None        # Recurrence start
    end_date: Optional[date] = None          # Recurrence end

class Task(BaseModel):
    _id: Optional[str] = None
    title: str
    description: Optional[str] = None
    due_date: date
    due_time: time
    linked_to: Optional[LinkedReference] = None

class Event(BaseModel):
    _id: Optional[str] = None
    title: str
    location: str
    event_date: date
    start_time: time
    end_time: time
    recurring: Optional[RecurringConfig] = None

class Class(BaseModel):
    _id: Optional[str] = None
    title: str
    online: bool = False
    location: str
    room: Optional[str] = None
    class_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    recurring: Optional[RecurringConfig] = None
    

class User(BaseModel):
    email: str
    password: str
    classes: List[Class] = []
    events: List[Event] = []
    tasks: List[Task] = []