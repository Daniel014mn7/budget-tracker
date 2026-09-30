from typing import Tuple, Optional, List, Dict

# allow running as package or single-file
try:
    from .utils import new_id, is_valid_date, parse_amount, find_index_by_id
    from .storage import CSVStorage
except ImportError:
    from utils import new_id, is_valid_date, parse_amount, find_index_by_id
    from storage import CSVStorage

class BudgetTracker:
    def __init__(self, storage: CSVStorage):
        self.storage = storage
        self.rows: List[Dict] = []
        ok, msg, data = self.storage.load()
        if not ok and data == []:
            print(f"[Warn] {msg}")
        else:
            print(f"[Info] {msg}")
        self.rows = data

    def add_income(self, date_str, amount_str, category="paycheck", notes="") -> Tuple[bool, str, Optional[int]]:
        if not is_valid_date(date_str):
            return False, "Invalid date format (YYYY-MM-DD).", None
        try:
            amount = parse_amount(amount_str)
        except ValueError as e:
            return False, str(e), None
        tid = new_id(self.rows)
        self.rows.append({
            "id": tid,
            "kind": "income",
            "date": date_str,
            "amount": amount,
            "category": category or "paycheck",
            "notes": notes or "",
        })
        return True, "Income added.", tid

    def add_expense(self, date_str, amount_str, category, notes="") -> Tuple[bool, str, Optional[int]]:
        if not is_valid_date(date_str):
            return False, "Invalid date format (YYYY-MM-DD).", None
        try:
            amount = parse_amount(amount_str)
        except ValueError as e:
            return False, str(e), None
        if not category:
            category = "Other"
        tid = new_id(self.rows)
        self.rows.append({
            "id": tid,
            "kind": "expense",
            "date": date_str,
            "amount": amount,
            "category": category,
            "notes": notes or "",
        })
        return True, "Expense added.", tid

    def edit_transaction(self, tid: int, **changes) -> Tuple[bool, str]:
        idx = find_index_by_id(self.rows, tid)
        if idx == -1:
            return False, "Transaction not found."
        tr = self.rows[idx].copy()

        if "date" in changes:
            if not is_valid_date(changes["date"]):
                return False, "Invalid date format (YYYY-MM-DD)."
            tr["date"] = changes["date"]

        if "amount" in changes:
            try:
                amt = parse_amount(changes["amount"])
            except ValueError as e:
                return False, str(e)
            tr["amount"] = amt

        if "category" in changes:
            tr["category"] = changes["category"] or tr.get("category", "Other")

        if "notes" in changes:
            tr["notes"] = str(changes["notes"])

        self.rows[idx] = tr
        return True, "Transaction updated."

    def delete_transaction(self, tid: int) -> Tuple[bool, str]:
        idx = find_index_by_id(self.rows, tid)
        if idx == -1:
            return False, "Transaction not found."
        self.rows.pop(idx)
        return True, "Transaction deleted."

    def compute_balance(self) -> float:
        inc = sum(t["amount"] for t in self.rows if t["kind"] == "income")
        exp = sum(t["amount"] for t in self.rows if t["kind"] == "expense")
        return round(inc - exp, 2)

    def monthly_summary(self, ym: str) -> Dict[str, float]:
        inc = 0.0
        exp = 0.0
        for t in self.rows:
            if str(t["date"])[:7] == ym:
                if t["kind"] == "income":
                    inc += t["amount"]
                else:
                    exp += t["amount"]
        return {"income": round(inc, 2), "expense": round(exp, 2), "net": round(inc - exp, 2)}

    def save(self) -> Tuple[bool, str]:
        return self.storage.save(self.rows)

    def reload(self) -> Tuple[bool, str, List[dict]]:
        ok, msg, rows = self.storage.load()
        if ok:
            self.rows = rows
        return ok, msg, rows
