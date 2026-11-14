"""
16 - Calculator App
===================
A desktop calculator with clickable buttons, built with tkinter.

Concepts you'll practise:
  - Laying out a grid of buttons with .grid(row=, column=, columnspan=)
  - StringVar: a variable the screen watches and redraws automatically
  - STATE: a calculator must remember the first number and the operator
    while you type the second number
  - The lambda default-argument trick:  command=lambda key=label: self.press(key)
    (without "key=label", every button would use the LAST label in the loop!)
  - Why we DON'T use eval(): it would run any Python code typed into it

Run:  python 16_calculator_app.py

Challenges:
  1. Keyboard support: root.bind("<Key>", ...) so you can type numbers.
  2. Add a backspace button.
  3. Show the pending calculation (e.g. "12 +") in a small label above the display.
"""
import tkinter as tk

OPERATORS = {"+", "-", "×", "÷"}

# (label, row, column, columnspan)
BUTTONS = [
    ("C", 1, 0, 1), ("±", 1, 1, 1), ("%", 1, 2, 1), ("÷", 1, 3, 1),
    ("7", 2, 0, 1), ("8", 2, 1, 1), ("9", 2, 2, 1), ("×", 2, 3, 1),
    ("4", 3, 0, 1), ("5", 3, 1, 1), ("6", 3, 2, 1), ("-", 3, 3, 1),
    ("1", 4, 0, 1), ("2", 4, 1, 1), ("3", 4, 2, 1), ("+", 4, 3, 1),
    ("0", 5, 0, 2), (".", 5, 2, 1), ("=", 5, 3, 1),
]


def format_number(value):
    """5.0 -> '5', 0.30000000000000004 -> '0.3'"""
    if value.is_integer() and abs(value) < 1e15:
        return str(int(value))
    return f"{value:.10g}"


class Calculator:
    def __init__(self, root):
        root.title("Calculator")
        root.resizable(False, False)

        # --- the calculator's memory ---
        self.display = tk.StringVar(value="0")
        self.stored = None        # first number, saved when an operator is pressed
        self.operator = None      # operator waiting to be applied
        self.start_new = False    # True when the next digit should start a fresh number

        # --- the screen ---
        screen = tk.Entry(root, textvariable=self.display, font=("Arial", 28),
                          justify="right", state="readonly", bd=0,
                          readonlybackground="white")
        screen.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=8, pady=8, ipady=10)

        # --- the buttons ---
        for label, row, col, span in BUTTONS:
            button = tk.Button(root, text=label, font=("Arial", 18), width=4, height=2,
                               command=lambda key=label: self.press(key))
            button.grid(row=row, column=col, columnspan=span, sticky="nsew", padx=2, pady=2)

    # ---------- one entry point for every button ----------
    def press(self, key):
        if self.display.get() == "Error" and key != "C":
            self.clear()
        if key.isdigit():
            self.add_digit(key)
        elif key == ".":
            self.add_decimal_point()
        elif key in OPERATORS:
            self.choose_operator(key)
        elif key == "=":
            self.calculate()
        elif key == "C":
            self.clear()
        elif key == "±":
            self.display.set(format_number(-float(self.display.get())))
        elif key == "%":
            self.display.set(format_number(float(self.display.get()) / 100))

    # ---------- the actions ----------
    def add_digit(self, digit):
        current = self.display.get()
        if self.start_new or current == "0":
            self.display.set(digit)
            self.start_new = False
        else:
            self.display.set(current + digit)

    def add_decimal_point(self):
        if self.start_new:
            self.display.set("0.")
            self.start_new = False
        elif "." not in self.display.get():
            self.display.set(self.display.get() + ".")

    def choose_operator(self, operator):
        if self.operator is not None and not self.start_new:
            self.calculate()                 # chaining: 2 + 3 + shows 5 straight away
            if self.display.get() == "Error":
                return
        self.stored = float(self.display.get())
        self.operator = operator
        self.start_new = True

    def calculate(self):
        if self.operator is None:
            return
        a = self.stored
        b = float(self.display.get())
        if self.operator == "+":
            result = a + b
        elif self.operator == "-":
            result = a - b
        elif self.operator == "×":
            result = a * b
        else:  # "÷"
            if b == 0:
                self.show_error()
                return
            result = a / b
        self.display.set(format_number(result))
        self.stored = None
        self.operator = None
        self.start_new = True

    def show_error(self):
        self.display.set("Error")
        self.stored = None
        self.operator = None
        self.start_new = True

    def clear(self):
        self.display.set("0")
        self.stored = None
        self.operator = None
        self.start_new = False


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
