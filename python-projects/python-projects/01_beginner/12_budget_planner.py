"""
12 - Budget Planner
===================
Set a monthly income and a budget for each category, record what you
actually spend, and see planned vs actual with a variance report.
Data is saved to budget.json.

Concepts you'll practise:
  - A nested dictionary saved as JSON:
      {"income": 5000, "categories": {"Rent": {"planned": 1800, "actual": 1800}}}
  - dict.setdefault() to create a key only if it doesn't exist yet
  - Percentages and variance (planned - actual) - same logic as a finance report
  - Aligned columns with f-string widths: {value:>11,.2f}
  - Text "bar charts" built from characters

Run:  python 12_budget_planner.py

Challenges:
  1. Add an option to delete a category.
  2. Sort the report so the most over-budget category is at the top.
  3. Keep a separate record for each month (hint: key the data by "2026-11").
"""
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("budget.json")

MENU = """
=== Budget Planner ===
  1. Set monthly income
  2. Add / update a category budget
  3. Record spending
  4. View budget report
  5. Show 50/30/20 guideline
  6. Start a new month (reset spending to zero)
  0. Quit"""


# ---------- saving and loading ----------
def load_budget():
    if DATA_FILE.exists():
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"income": 0.0, "categories": {}}


def save_budget(budget):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(budget, f, indent=2)


# ---------- helpers ----------
def ask_amount(prompt):
    while True:
        try:
            value = float(input(prompt).replace(",", ""))
        except ValueError:
            print("  Numbers only, please.")
            continue
        if value >= 0:
            return round(value, 2)
        print("  Amount can't be negative.")


def pick_category(budget):
    names = list(budget["categories"])
    if not names:
        print("  Add a category first (option 2).")
        return None
    for i, name in enumerate(names, start=1):
        print(f"  {i}. {name}")
    text = input("Category number: ").strip()
    if text.isdigit() and 1 <= int(text) <= len(names):
        return names[int(text) - 1]
    print("  Invalid choice.")
    return None


def progress_bar(fraction, width=20):
    filled = min(round(fraction * width), width)
    return "#" * filled + "-" * (width - filled)


# ---------- actions ----------
def set_income(budget):
    budget["income"] = ask_amount("Monthly income (after tax): ")


def set_category(budget):
    name = input("Category name (e.g. Rent, Groceries): ").strip().title()
    if not name:
        return
    category = budget["categories"].setdefault(name, {"planned": 0.0, "actual": 0.0})
    category["planned"] = ask_amount(f"Planned monthly budget for {name}: ")


def record_spending(budget):
    name = pick_category(budget)
    if name:
        amount = ask_amount(f"Amount spent on {name}: ")
        budget["categories"][name]["actual"] += amount
        cat = budget["categories"][name]
        print(f"  {name}: {cat['actual']:,.2f} spent of {cat['planned']:,.2f} planned.")


def show_report(budget):
    categories = budget["categories"]
    if not categories:
        print("\n  Nothing to show yet. Add a category first.")
        return

    line = "-" * 86
    print(f"\n{'Category':<16}{'Planned':>11}{'Actual':>11}{'Left':>11}{'Used':>7}")
    print(line)
    total_planned = total_actual = 0.0
    for name, c in categories.items():
        planned, actual = c["planned"], c["actual"]
        left = planned - actual
        used = actual / planned if planned else (1.0 if actual else 0.0)
        flag = "  OVER!" if actual > planned else ""
        print(f"{name[:15]:<16}{planned:>11,.2f}{actual:>11,.2f}{left:>11,.2f}"
              f"{used:>7.0%}  {progress_bar(used)}{flag}")
        total_planned += planned
        total_actual += actual
    print(line)
    print(f"{'TOTAL':<16}{total_planned:>11,.2f}{total_actual:>11,.2f}"
          f"{total_planned - total_actual:>11,.2f}")

    income = budget["income"]
    if income:
        print(f"\n  Income:             {income:>12,.2f}")
        print(f"  Planned spending:   {total_planned:>12,.2f}  ({total_planned / income:.0%} of income)")
        print(f"  Not yet allocated:  {income - total_planned:>12,.2f}")
        print(f"  Left after spending:{income - total_actual:>12,.2f}")
    else:
        print("\n  Tip: set your income (option 1) to see how much is unallocated.")


def show_guideline(budget):
    income = budget["income"]
    if not income:
        print("  Set your income first (option 1).")
        return
    print("\n  The 50/30/20 rule of thumb splits income into:")
    for label, share in [("Needs (rent, bills, food)", 0.5),
                         ("Wants (dining, hobbies)", 0.3),
                         ("Savings / debt repayment", 0.2)]:
        print(f"    {label:<28}{share:>5.0%}  {income * share:>12,.2f}")


def reset_month(budget):
    if input("Reset all spending to zero? (y/n): ").strip().lower() == "y":
        for c in budget["categories"].values():
            c["actual"] = 0.0
        print("  New month started. Your planned budgets are kept.")


def main():
    budget = load_budget()
    actions = {"1": set_income, "2": set_category, "3": record_spending,
               "4": show_report, "5": show_guideline, "6": reset_month}
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "0":
            print("Bye!")
            break
        action = actions.get(choice)     # a dictionary of FUNCTIONS replaces a long if/elif
        if action:
            action(budget)
            save_budget(budget)
        else:
            print("  Please choose from the menu.")


if __name__ == "__main__":
    main()
