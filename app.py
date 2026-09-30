
from pathlib import Path

# allow running as package or single-file
try:
    from .storage import CSVStorage
    from .tracker import BudgetTracker
except ImportError:
    from storage import CSVStorage
    from tracker import BudgetTracker

DATA_PATH = Path("budget_data.csv")  # use your same CSV file name

def prompt(msg: str) -> str:
    return input(msg).strip()

def main():
    storage = CSVStorage(DATA_PATH)
    bt = BudgetTracker(storage)

    while True:
        print("\n=== Budget Tracker — Part 5 ===")
        print("1) Add income")
        print("2) Add expense")
        print("3) Edit transaction")
        print("4) Delete transaction")
        print("5) Compute balance")
        print("6) Monthly summary (YYYY-MM)")
        print("7) Save to CSV")
        print("8) Reload from CSV")
        print("0) Exit")
        option = prompt("Choose: ")

        try:
            if option == "1":
                d = prompt("date (YYYY-MM-DD): ")
                a = prompt("amount (e.g., 1200.00): ")
                c = prompt("category [paycheck]: ") or "paycheck"
                n = prompt("notes [optional]: ")
                ok, msg, tid = bt.add_income(d, a, c, n)
                print(msg, "| id:", tid)

            elif option == "2":
                d = prompt("date (YYYY-MM-DD): ")
                a = prompt("amount (e.g., 60.25): ")
                c = prompt("category: ")
                n = prompt("notes [optional]: ")
                ok, msg, tid = bt.add_expense(d, a, c, n)
                print(msg, "| id:", tid)

            elif option == "3":
                tid = int(prompt("transaction id: "))
                print("Leave empty to skip a field.")
                nd = prompt("new date (YYYY-MM-DD): ")
                na = prompt("new amount: ")
                nc = prompt("new category: ")
                nn = prompt("new notes: ")
                changes = {}
                if nd: changes["date"] = nd
                if na: changes["amount"] = na
                if nc: changes["category"] = nc
                if nn: changes["notes"] = nn
                ok, msg = bt.edit_transaction(tid, **changes)
                print(msg)

            elif option == "4":
                tid = int(prompt("transaction id: "))
                ok, msg = bt.delete_transaction(tid)
                print(msg)

            elif option == "5":
                print("Balance:", bt.compute_balance())

            elif option == "6":
                ym = prompt("year-month (YYYY-MM): ")
                print("Summary:", bt.monthly_summary(ym))

            elif option == "7":
                ok, msg = bt.save()
                print(msg)

            elif option == "8":
                ok, msg, _ = bt.reload()
                print(msg)

            elif option == "0":
                print("Bye!")
                break

            else:
                print("Invalid option.")
        except Exception as e:
            print("[Error]", e)

if __name__ == "__main__":
    main()
