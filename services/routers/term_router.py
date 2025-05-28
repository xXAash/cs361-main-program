from fastapi import APIRouter
from services.utils.term_dates_generator import generate_term_dates

router = APIRouter()

@router.get("/api/term-dates/{term}/{year}")
def get_term_dates(term: str, year: int):
    try:
        start_date, end_date = generate_term_dates(term.lower(), int(year))
        return {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    except ValueError as e:
        return {"error": str(e)}
