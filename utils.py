from datetime import datetime

CSV_HEADER = ["id", "kind", "date", "amount", "category", "notes"]
VALID_KINDS = {"income", "expense"}
DATE_FMT = "%Y-%m-%d"

def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(str(date_str), DATE_FMT)
        return True
    except Exception:
        return False

def parse_amount(amount_str: str) -> float:
    try:
        v = float(amount_str)
        if v <= 0:
            raise ValueError
        return round(v, 2)
    except Exception:
        raise ValueError("Invalid amount (use numbers like 125.90).")

def new_id(rows: list) -> int:
    return 1 if not rows else max(t["id"] for t in rows) + 1

def find_index_by_id(rows: list, tid: int) -> int:
    for i, t in enumerate(rows):
        if t.get("id") == tid:
            return i
    return -1
