"""
10 - Contact Book
=================
Add, view, search, edit and delete contacts. Saved to contacts.csv,
which you can also open in Excel.

Concepts you'll practise:
  - The csv module: DictReader (read rows as dictionaries) and DictWriter
  - Case-insensitive search with .lower() and the any(...) function
  - Simple validation functions that return True / False
  - Passing a FUNCTION as an argument (the `validator` parameter in ask())
  - "Press Enter to keep the current value" - a common editing pattern

Run:  python 10_contact_book.py

Challenges:
  1. Always show contacts sorted by name.
  2. Stop the user adding two contacts with the same name.
  3. Add a "company" field. What breaks with your existing contacts.csv, and why?
"""
import csv
from pathlib import Path

DATA_FILE = Path(__file__).with_name("contacts.csv")
FIELDS = ["name", "phone", "email"]

MENU = """
=== Contact Book ===
  1. View all
  2. Add contact
  3. Search
  4. Edit contact
  5. Delete contact
  0. Quit"""


# ---------- saving and loading ----------
def load_contacts():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_contacts(contacts):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(contacts)


# ---------- validation ----------
def is_valid_name(name):
    return name != ""


def is_valid_phone(phone):
    allowed = set("0123456789+-() ")
    digit_count = sum(ch.isdigit() for ch in phone)
    return set(phone) <= allowed and digit_count >= 7


def is_valid_email(email):
    if email == "":
        return True                      # email is optional
    if email.count("@") != 1:
        return False
    local, domain = email.split("@")
    return bool(local) and "." in domain.strip(".")


def ask(prompt, validator, error, current=None):
    """Ask for a value until `validator(value)` is True.
    If `current` is given, pressing Enter keeps the current value."""
    hint = f" [{current}]" if current else ""
    while True:
        value = input(f"{prompt}{hint}: ").strip()
        if value == "" and current is not None:
            return current
        if validator(value):
            return value
        print(f"  {error}")


def ask_details(existing=None):
    existing = existing or {"name": None, "phone": None, "email": None}
    return {
        "name": ask("Name", is_valid_name, "Name can't be empty.", existing["name"]),
        "phone": ask("Phone", is_valid_phone, "Use digits (at least 7), spaces, + - ( ).",
                     existing["phone"]),
        "email": ask("Email (optional)", is_valid_email, "That doesn't look like an email.",
                     existing["email"]),
    }


# ---------- display ----------
def print_contacts(contacts):
    if not contacts:
        print("\n  No contacts found.")
        return
    print(f"\n  {'#':>3}  {'Name':<25}{'Phone':<18}Email")
    for i, c in enumerate(contacts, start=1):
        print(f"  {i:>3}. {c['name']:<25}{c['phone']:<18}{c['email']}")


def choose_contact(contacts, verb):
    print_contacts(contacts)
    if not contacts:
        return None
    text = input(f"Number of the contact to {verb}: ").strip()
    if text.isdigit() and 1 <= int(text) <= len(contacts):
        return int(text) - 1
    print("  Invalid number.")
    return None


# ---------- main program ----------
def main():
    contacts = load_contacts()
    while True:
        print(MENU)
        choice = input("Choose: ").strip()

        if choice == "1":
            print_contacts(contacts)
        elif choice == "2":
            contacts.append(ask_details())
            save_contacts(contacts)
            print("  Contact saved.")
        elif choice == "3":
            term = input("Search for: ").strip().lower()
            matches = [c for c in contacts
                       if any(term in c[field].lower() for field in FIELDS)]
            print_contacts(matches)
        elif choice == "4":
            i = choose_contact(contacts, "edit")
            if i is not None:
                print("  (Press Enter to keep the current value)")
                contacts[i] = ask_details(contacts[i])
                save_contacts(contacts)
                print("  Contact updated.")
        elif choice == "5":
            i = choose_contact(contacts, "delete")
            if i is not None:
                name = contacts[i]["name"]
                if input(f"Delete {name}? (y/n): ").strip().lower() == "y":
                    contacts.pop(i)
                    save_contacts(contacts)
                    print(f"  Deleted {name}.")
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("  Please choose from the menu.")


if __name__ == "__main__":
    main()
