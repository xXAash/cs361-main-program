from datetime import datetime, date

def generate_term_dates(term: str, year: int) -> tuple[date, date]:
    term_dates = {
        "fall":    {"start": f"{year}-09-25", "end": f"{year}-12-13"},
        "winter":  {"start": f"{year}-01-02", "end": f"{year}-03-13"},
        "spring":  {"start": f"{year}-03-31", "end": f"{year}-06-13"},
        "summer":  {"start": f"{year}-06-23", "end": f"{year}-09-05"},
    }

    if term not in term_dates:
        raise ValueError(f"Invalid term: {term}")

    start_str = term_dates[term]["start"]
    end_str = term_dates[term]["end"]

    start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_str, "%Y-%m-%d").date()

    return start_date, end_date