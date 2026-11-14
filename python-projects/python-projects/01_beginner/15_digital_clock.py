"""
15 - Digital Clock
==================
Your first GUI (window) app: a live digital clock with the date.
Click the time to switch between 12-hour and 24-hour format.

Concepts you'll practise:
  - tkinter, Python's built-in GUI toolkit: Tk(), Label, pack()
  - A class to keep the window and its state (self.use_24h) together
  - root.after(1000, function): "run this again in 1 second".
    GUIs use this INSTEAD of while-loops + sleep (a while-loop would freeze the window).
  - Events: bind("<Button-1>", ...) runs a function when you click
  - strftime() codes: %H %I %M %S %p %A %d %B %Y

Run:  python 15_digital_clock.py

Challenges:
  1. Add a button that switches between a dark and a light theme.
  2. Show a second clock for another time zone (look up zoneinfo).
  3. Add a stopwatch with Start / Stop / Reset buttons.
"""
import tkinter as tk
from datetime import datetime

BACKGROUND = "#101010"
TIME_COLOUR = "#39FF14"      # neon green


class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.use_24h = True

        root.title("Digital Clock")
        root.configure(bg=BACKGROUND)
        root.resizable(False, False)

        self.time_label = tk.Label(root, font=("Consolas", 60, "bold"),
                                   fg=TIME_COLOUR, bg=BACKGROUND, cursor="hand2")
        self.time_label.pack(padx=30, pady=(20, 0))

        self.date_label = tk.Label(root, font=("Consolas", 18), fg="white", bg=BACKGROUND)
        self.date_label.pack()

        hint = tk.Label(root, text="Click the time to switch 12h / 24h",
                        font=("Consolas", 10), fg="gray", bg=BACKGROUND)
        hint.pack(pady=(4, 15))

        self.time_label.bind("<Button-1>", self.toggle_format)
        self.tick()

    def update_display(self):
        now = datetime.now()
        time_format = "%H:%M:%S" if self.use_24h else "%I:%M:%S %p"
        self.time_label.config(text=now.strftime(time_format))
        self.date_label.config(text=now.strftime("%A, %d %B %Y"))

    def tick(self):
        self.update_display()
        self.root.after(1000, self.tick)       # schedule the next tick

    def toggle_format(self, event=None):
        self.use_24h = not self.use_24h
        self.update_display()                  # redraw now (don't start a 2nd tick loop!)


if __name__ == "__main__":
    root = tk.Tk()
    DigitalClock(root)
    root.mainloop()        # hands control to tkinter until the window is closed
