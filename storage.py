import csv
import sqlite3
from typing import List, Tuple
from pathlib import Path

# Allow running as package or single-file
try:
    from .models import Transaction
    from .utils import CSV_HEADER, VALID_KINDS, is_valid_date
except ImportError:
    from models import Transaction
    from utils import CSV_HEADER, VALID_KINDS, is_valid_date


class CSVStorage:
    def __init__(self, path: Path):
        self.path = path
        # Database file with the same base name as the CSV
        self.db_path = self.path.with_suffix(".db")
        # Make sure the database and table exist
        self._init_db()

    def _init_db(self) -> None:
        """Create the database and the transactions table if they don't exist."""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY,
                    kind TEXT NOT NULL,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT,
                    notes TEXT
                )
                """
            )
            conn.commit()
        except Exception:
            # If something goes wrong here, the rest of the program can still run
            pass
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def load(self) -> Tuple[bool, str, List[dict]]:
        """
        Load all data. The program tries the database first.
        If the database is empty, it falls back to the CSV file.
        """
        rows: List[dict] = []

        # Try loading from SQLite first
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(
                "SELECT id, kind, date, amount, category, notes FROM transactions ORDER BY id"
            )
            db_rows = cur.fetchall()
            conn.close()

            # If the database has data, use it
            if db_rows:
                for tid, kind, date_str, amount, category, notes in db_rows:
                    if kind not in VALID_KINDS:
                        continue
                    if not is_valid_date(date_str):
                        continue

                    try:
                        amount_f = float(amount)
                    except Exception:
                        continue

                    rows.append({
                        "id": int(tid),
                        "kind": kind,
                        "date": str(date_str),
                        "amount": round(amount_f, 2),
                        "category": category or "",
                        "notes": notes or "",
                    })

                return True, "Loaded from SQLite database.", rows

        except Exception:
            # If database loading fails, move on and try CSV
            rows = []

        # Load from CSV if the database was empty or failed
        try:
            with open(self.path, "r", encoding="utf-8", newline="") as f:
                r = csv.reader(f)
                header = next(r, None)

                # Check if the CSV header is correct
                if header != CSV_HEADER:
                    return False, "Invalid or corrupted CSV file.", []

                rows = []
                for row in r:
                    if len(row) != 6:
                        return False, "Invalid row length in CSV.", []

                    tid_s, kind, date_str, amount_s, category, notes = row

                    try:
                        tid = int(tid_s)
                        if kind not in VALID_KINDS:
                            return False, "Invalid 'kind' in CSV.", []
                        if not is_valid_date(date_str):
                            return False, "Invalid 'date' in CSV.", []
                        amount = float(amount_s)
                    except Exception:
                        return False, "Invalid value type in CSV.", []

                    rows.append({
                        "id": tid,
                        "kind": kind,
                        "date": date_str,
                        "amount": round(amount, 2),
                        "category": category,
                        "notes": notes,
                    })

                return True, "Loaded from CSV.", rows

        except FileNotFoundError:
            return True, "No data file found, starting empty.", []
        except OSError:
            return False, "Could not access the file (check path/permissions).", []
        except csv.Error:
            return False, "Invalid or corrupted CSV file.", []

    def save(self, rows: List[dict]) -> Tuple[bool, str]:
        """
        Save data. First to the SQLite database.
        Then also write a CSV copy for backup/export.
        """
        # Save to the database
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            # Clear old data before saving new data
            cur.execute("DELETE FROM transactions")

            for t in rows:
                cur.execute(
                    "INSERT INTO transactions (id, kind, date, amount, category, notes) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        int(t["id"]),
                        t["kind"],
                        str(t["date"]),
                        float(t["amount"]),
                        t.get("category", ""),
                        t.get("notes", ""),
                    ),
                )

            conn.commit()
            conn.close()

        except Exception:
            return False, "Could not save to SQLite database."

        # Save a CSV copy
        try:
            with open(self.path, "w", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                w.writerow(CSV_HEADER)
                for t in rows:
                    w.writerow([
                        t["id"], t["kind"], str(t["date"]),
                        f"{float(t['amount']):.2f}",
                        t.get("category", ""), t.get("notes", "")
                    ])
            return True, "Saved to database and CSV."
        except OSError:
            # Database save worked, but CSV failed
            return True, "Saved to database, but could not access the CSV file."
