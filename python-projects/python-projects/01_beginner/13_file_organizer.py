"""
13 - File Organizer
===================
Tidies a messy folder (like Downloads) by moving files into sub-folders
by type: Images, Documents, Spreadsheets, Video, ...

SAFETY: it shows you a preview first and only moves files if you say yes.
It never overwrites anything: duplicates become "report (1).pdf".

Concepts you'll practise:
  - pathlib: .iterdir(), .suffix, .stem, .is_file(), .mkdir()
  - shutil.move() to move files
  - "Plan first, act second" (a dry run) - always do this when code changes files
  - collections.Counter for quick counts

Run:  python 13_file_organizer.py
Tip: test it on a COPY of a folder the first time.

Challenges:
  1. Add an "undo" that moves everything back (hint: save the moves to a JSON file).
  2. Organise by year/month of the file's modified date instead of by type.
  3. Let the user pass the folder on the command line (look up sys.argv or argparse).
"""
import shutil
from collections import Counter
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"},
    "Spreadsheets": {".xls", ".xlsx", ".xlsm", ".csv"},
    "Presentations": {".ppt", ".pptx", ".key"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".m4a"},
    "Video": {".mp4", ".mov", ".avi", ".mkv", ".wmv"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".ipynb", ".js", ".html", ".css", ".sql", ".json"},
    "Installers": {".exe", ".msi", ".dmg", ".pkg"},
}


def category_for(path):
    extension = path.suffix.lower()          # "Report.PDF" -> ".pdf"
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"


def unique_destination(destination):
    """If the destination already exists, add (1), (2)... so we never overwrite."""
    if not destination.exists():
        return destination
    counter = 1
    while True:
        candidate = destination.with_name(f"{destination.stem} ({counter}){destination.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def plan_moves(folder):
    """Return a list of (source, destination) pairs. Nothing is moved here."""
    this_script = Path(__file__).resolve()
    moves = []
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue                         # skip folders and hidden files
        if item.resolve() == this_script:
            continue                         # don't move ourselves!
        moves.append((item, folder / category_for(item) / item.name))
    return moves


def main():
    print("=== File Organizer ===")
    text = input("Folder to organise (paste the path): ").strip().strip('"')
    folder = Path(text).expanduser()
    if not folder.is_dir():
        print("  That folder doesn't exist.")
        return

    moves = plan_moves(folder)
    if not moves:
        print("  No files to organise.")
        return

    print(f"\nPreview: {len(moves)} file(s) would be moved:")
    for source, destination in moves:
        print(f"  {source.name:<45} -> {destination.parent.name}/")

    if input("\nMove these files? (y/n): ").strip().lower() != "y":
        print("No files were moved.")
        return

    for source, destination in moves:
        destination.parent.mkdir(exist_ok=True)
        shutil.move(str(source), str(unique_destination(destination)))

    counts = Counter(destination.parent.name for _, destination in moves)
    print("\nDone! Files moved:")
    for category, count in counts.most_common():
        print(f"  {category:<15}{count}")


if __name__ == "__main__":
    main()
