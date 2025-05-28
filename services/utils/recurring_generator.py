from datetime import date, time, timedelta
from typing import List

weekday_map = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

def generate_recurring_items(
    title: str,
    location: str,
    start_time: time,
    end_time: time,
    days: List[str],
    start_date: date,
    end_date: date,
    item_type: str = "event",  # or "class"
    extras: dict = {}
) -> List[dict]:
    result = []
    delta = timedelta(days=1)
    current = start_date

    day_nums = [weekday_map[day] for day in days]

    while current <= end_date:
        if current.weekday() in day_nums:
            entry = {
                "title": title,
                "location": location,
                "start_time": start_time,
                "end_time": end_time,
                "_id": None,  # filled later
            }

            if item_type == "event":
                entry["event_date"] = current
            elif item_type == "class":
                entry["class_date"] = current
                entry["room"] = extras.get("room")
                entry["online"] = extras.get("online", False)

            result.append(entry)
        current += delta

    return result
