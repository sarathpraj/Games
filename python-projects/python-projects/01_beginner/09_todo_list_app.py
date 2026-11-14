"""
09 - To-Do List
===============
Add, tick off and delete tasks. Your list is saved to todos.json,
so it's still there next time you run the program.

Concepts you'll practise:
  - A list of dictionaries: each task is {"title": ..., "done": ..., "added": ...}
  - Saving and loading data with the json module
  - pathlib.Path for file locations (works on Windows AND Mac)
  - CRUD: Create, Read, Update, Delete - the four basic data operations
  - List comprehensions as filters: [t for t in tasks if not t["done"]]

Run:  python 09_todo_list_app.py
Then open todos.json in a text editor to see how your data is stored.

Challenges:
  1. Add a priority (high / medium / low) and sort the list by it.
  2. Add a due date and show overdue tasks in their own section.
  3. Let the user edit a task's title.
"""
import json
from datetime import date
from pathlib import Path

# Save the file next to this script, wherever you run it from
DATA_FILE = Path(__file__).with_name("todos.json")

MENU = """
=== To-Do List ===
  1. Show tasks
  2. Add task
  3. Mark task done / not done
  4. Delete task
  5. Clear completed tasks
  0. Quit"""


def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)       # indent=2 makes the file human-readable


def show_tasks(tasks):
    if not tasks:
        print("\n  Your list is empty.")
        return
    print()
    for i, task in enumerate(tasks, start=1):
        box = "[x]" if task["done"] else "[ ]"
        print(f"  {i:>2}. {box} {task['title']}   (added {task['added']})")
    remaining = sum(1 for t in tasks if not t["done"])
    print(f"\n  {remaining} of {len(tasks)} task(s) still to do.")


def choose_task(tasks, verb):
    """Show the list and return the index of the chosen task, or None."""
    if not tasks:
        print("\n  Your list is empty.")
        return None
    show_tasks(tasks)
    text = input(f"Which task number to {verb}? ").strip()
    if text.isdigit() and 1 <= int(text) <= len(tasks):
        return int(text) - 1                 # people count from 1, Python from 0
    print("  That number isn't on the list.")
    return None


def main():
    tasks = load_tasks()
    while True:
        print(MENU)
        choice = input("Choose: ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            title = input("Task: ").strip()
            if title:
                tasks.append({"title": title, "done": False, "added": date.today().isoformat()})
                save_tasks(tasks)
                print("  Added.")
        elif choice == "3":
            i = choose_task(tasks, "tick / untick")
            if i is not None:
                tasks[i]["done"] = not tasks[i]["done"]
                save_tasks(tasks)
        elif choice == "4":
            i = choose_task(tasks, "delete")
            if i is not None:
                removed = tasks.pop(i)
                save_tasks(tasks)
                print(f"  Deleted: {removed['title']}")
        elif choice == "5":
            before = len(tasks)
            tasks = [t for t in tasks if not t["done"]]
            save_tasks(tasks)
            print(f"  Removed {before - len(tasks)} completed task(s).")
        elif choice == "0":
            print(f"Bye! Your tasks are saved in {DATA_FILE.name}")
            break
        else:
            print("  Please choose from the menu.")


if __name__ == "__main__":
    main()
