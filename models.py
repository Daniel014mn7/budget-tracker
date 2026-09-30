from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass
class Transaction:
    id: int
    kind: str          # 'income' or 'expense'
    date: str          # YYYY-MM-DD
    amount: float
    category: str
    notes: str = ""

    def to_csv_row(self) -> List[str]:
        return [str(self.id), self.kind, self.date, f"{self.amount:.2f}", self.category, self.notes]

    @staticmethod
    def csv_header() -> List[str]:
        return ["id", "kind", "date", "amount", "category", "notes"]

    def to_dict(self) -> Dict:
        return asdict(self)
