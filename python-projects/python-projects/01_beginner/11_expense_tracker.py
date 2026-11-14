"""
11 - Expense Tracker
====================
Log your spending and see totals by category and by month.
Data is saved to expenses.csv (open it in Excel any time).

Concepts you'll practise:
  - Appending rows to a CSV file (mode "a") instead of rewriting it
  - Converting text to numbers after reading a CSV (CSV stores everything as text)
  - Dates: datetime.strptime() to check the format, date.today()
  - Grouping and totalling with collections.defaultdict - like a pivot table in code
  - Passing small functions (lambdas) to decide HOW to group

Run:  python 11_expense_tracker.py

Challenges:
  1. Add "delete last expense".
  2. Filter: show only one month, or only one category.
  3. Advanced: load expenses.csv with pandas and recreate the summaries in 3 lines.
"""
import csv
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["date", "category", "description", "amount"]
CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Health", "Other"]

MENU = """
=== Expense Tracker ===
  1. Add expense
  2. View all expenses
  3. Summary by category
  4. Summary by month
  0. Quit"""


# ---------- saving and loading ----------
def load_expenses():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        expenses = list(csv.DictReader(f))
    for e in expenses:
        e["amount"] = float(e["amount"])     # "12.50" -> 12.5
    return expenses


def append_expense(expense):
    new_file = not DATA_FILE.exists()
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:   # "a" = append
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()             # only write the header once
        writer.writerow(expense)


# ---------- input helpers ----------
def ask_date():
    while True:
        text = input("Date (YYYY-MM-DD) [today]: ").strip()
        if not text:
            return date.today().isoformat()
        try:
            return datetime.strptime(text, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print(f"  Please use the format YYYY-MM-DD, e.g. {date.today().isoformat()}")


def ask_category():
    for i, name in enumerate(CATEGORIES, start=1):
        print(f"  {i}. {name}")
    while True:
        text = input("Category number: ").strip()
        if text.isdigit() and 1 <= int(text) <= len(CATEGORIES):
            return CATEGORIES[int(text) - 1]
        print("  Please pick a number from the list.")


def ask_amount():
    while True:
        try:
            amount = float(input("Amount: ").replace(",", ""))
        except ValueError:
            print("  Numbers only, please.")
            continue
        if amount > 0:
            return round(amount, 2)
        print("  Amount must be more than zero.")


# ---------- actions ----------
def add_expense():
    expense = {
        "date": ask_date(),
        "category": ask_category(),
        "description": input("Description: ").strip() or "-",
        "amount": ask_amount(),
    }
    append_expense(expense)
    print(f"  Saved: {expense['amount']:,.2f} on {expense['category']}.")


def show_all(expenses):
    if not expenses:
        print("\n  No expenses yet.")
        return
    print(f"\n{'Date':<12}{'Category':<15}{'Description':<28}{'Amount':>12}")
    print("-" * 67)
    for e in sorted(expenses, key=lambda e: e["date"]):
        print(f"{e['date']:<12}{e['category']:<15}{e['description'][:26]:<28}{e['amount']:>12,.2f}")
    print("-" * 67)
    total = sum(e["amount"] for e in expenses)
    print(f"{'TOTAL':<55}{total:>12,.2f}")


def summarise(expenses, group_by, title, sort_by_amount=True):
    """Total the expenses by whatever group_by(expense) returns.
    One function, reused for 'by category' AND 'by month'."""
    if not expenses:
        print("\n  No expenses yet.")
        return
    totals = defaultdict(float)              # missing keys start at 0.0 automatically
    for e in expenses:
        totals[group_by(e)] += e["amount"]

    if sort_by_amount:
        rows = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    else:
        rows = sorted(totals.items())        # alphabetical / chronological
    grand_total = sum(totals.values())

    print(f"\n{title}")
    print("-" * 64)
    for key, amount in rows:
        share = amount / grand_total
        bar = "#" * round(share * 30)
        print(f"{key:<15}{amount:>12,.2f}{share:>6.0%}  {bar}")
    print("-" * 64)
    print(f"{'TOTAL':<15}{grand_total:>12,.2f}")


def main():
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            show_all(load_expenses())
        elif choice == "3":
            summarise(load_expenses(), lambda e: e["category"], "Spending by category")
        elif choice == "4":
            summarise(load_expenses(), lambda e: e["date"][:7], "Spending by month",
                      sort_by_amount=False)      # "2026-11-14"[:7] -> "2026-11"
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("  Please choose from the menu.")


if __name__ == "__main__":
    main()
