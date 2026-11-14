# Python Projects: Beginner Level

19 small Python projects. Every file can be run on its own, and each one is
commented to explain *why* the code is written the way it is, not just what it does.

The projects are in **learning order**, not the order of the original poster.
Each one reuses ideas from earlier ones and adds one or two new ones.

---

## 1. Setup (one time)

1. Install **Python 3.10 or newer** from [python.org](https://www.python.org/downloads/).
   On Windows, tick **"Add Python to PATH"** during install.
2. Check it works:
   ```
   python --version
   ```
3. Projects 01–16 and 19 use only Python's built-in libraries, so there is nothing to install.
4. Projects 17 and 18 need two extra libraries:
   ```
   pip install -r requirements.txt
   ```

## 2. Running a project

```
cd 01_beginner
python 01_number_guessing_game.py
```
You can also open any file in VS Code and press the ▶ Run button.

---

## 3. Learning path

| #  | Project            | New concepts                                              | Type      |
|----|--------------------|-----------------------------------------------------------|-----------|
| **Stage 1: Foundations** | | | |
| 01 | Number Guessing    | `random`, while loops, `input()`, `int()`, try/except     | Terminal  |
| 02 | Rock Paper Scissors| Dictionaries as rule tables, functions that return values | Terminal  |
| 03 | Password Generator | `string` & `secrets` modules, `"".join()`, default args   | Terminal  |
| 04 | Unit Converter     | Nested dictionaries, "convert via a base unit" pattern     | Terminal  |
| 05 | Currency Converter | Lookup tables, number formatting `{x:,.2f}`               | Terminal  |
| 06 | BMI Calculator     | Pure functions, floats, if/elif ranges, defensive checks  | Terminal  |
| **Stage 2: Data & state** | | | |
| 07 | Hangman            | Sets and set maths, generator expressions, raw strings    | Terminal  |
| 08 | Tic-Tac-Toe        | A list as a game board, tuple unpacking, simple game AI   | Terminal  |
| 09 | To-Do List         | List of dicts, **JSON save/load**, `pathlib`, CRUD        | Terminal  |
| **Stage 3: Working with files** | | | |
| 10 | Contact Book       | **CSV** read/write, search, validation, functions as args | Terminal  |
| 11 | Expense Tracker    | Appending to CSV, dates, grouping with `defaultdict`      | Terminal  |
| 12 | Budget Planner     | Nested JSON, variance %, dictionary of functions          | Terminal  |
| 13 | File Organizer     | `pathlib`, `shutil.move`, dry-run safety, `Counter`       | Terminal  |
| **Stage 4: Time** | | | |
| 14 | Alarm Clock        | `datetime`, `timedelta`, `time.sleep`, Ctrl+C handling    | Terminal  |
| **Stage 5: Desktop apps (GUI)** | | | |
| 15 | Digital Clock      | First `tkinter` window, classes, `after()` timer loop     | GUI       |
| 16 | Calculator App     | Button grids, `StringVar`, state machine, lambda trick    | GUI       |
| **Stage 6: Libraries & games** | | | |
| 17 | QR Code Generator  | Installing & using a third-party library (`qrcode`)       | Terminal  |
| 18 | Music Player       | tkinter + `pygame`, file dialogs, polling for events      | GUI       |
| 19 | Snake Game         | `turtle` graphics, game loop, collision detection         | GUI       |

---

## 4. How to learn from these (suggested routine per project)

1. **Run it** and play with it. Try to break it with silly input.
2. **Read the docstring** at the top, then read the code top to bottom.
3. **Rebuild it from scratch** in a new file (e.g. `my_01.py`) without looking.
   Peek only when you're stuck. This is where most of the learning happens.
4. **Do at least one Challenge** listed at the top of the file.
5. **Commit it to GitHub** (see below).

Debugging tip: if something doesn't work, add `print()` lines to see what your
variables contain, or use the debugger in VS Code (click left of a line number to
set a breakpoint, then press F5).

---

## 5. Save to GitHub

Create an **empty** repository called `python-projects` on GitHub first, then:

```
cd python-projects
git init
git add .
git commit -m "Add beginner Python projects"
git branch -M main
git remote add origin https://github.com/sarathpraj/python-projects.git
git push -u origin main
```

After each new project or challenge:
```
git add .
git commit -m "Hangman: add word categories"
git push
```

---

## 6. Files the projects create

Some projects save your data next to the script: `todos.json`, `contacts.csv`,
`expenses.csv`, `budget.json` and QR code `.png` images.
These are listed in `.gitignore`, so your personal data is **not** uploaded to GitHub.
