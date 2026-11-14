"""
06 - BMI Calculator
===================
Calculates Body Mass Index from height and weight, in metric or imperial units.

Note: BMI is a rough screening number for adults. It doesn't account for
muscle, age, sex or body shape, so treat it as a starting point only.

Concepts you'll practise:
  - "Pure" functions: same input -> same output, no input()/print() inside.
    They are the easiest kind of code to test.
  - Floats and rounding in f-strings: {value:.1f}
  - if / elif chains for number ranges
  - Defensive programming: spotting a likely user mistake and fixing it

Run:  python 06_bmi_calculator.py

Challenges:
  1. Write a quick test: assert round(calculate_bmi(70, 1.75), 1) == 22.9
  2. Save each result with today's date to a CSV file (you'll learn CSV in 10).
  3. After project 15, turn this into a small window with tkinter.
"""

KG_PER_POUND = 0.45359237
METRES_PER_INCH = 0.0254


def calculate_bmi(weight_kg, height_m):
    return weight_kg / height_m ** 2


def bmi_category(bmi):
    # Standard WHO adult categories
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Healthy weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity"


def ask_number(prompt, allow_zero=False):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("  Please enter a number.")
            continue
        if value > 0 or (allow_zero and value == 0):
            return value
        print("  Please enter a positive number.")


def get_measurements():
    """Ask for weight and height. Always returns (kg, metres)."""
    units = input("Units: 1) metric (kg, cm)   2) imperial (lb, ft/in): ").strip()
    if units == "2":
        pounds = ask_number("Weight in pounds: ")
        feet = ask_number("Height - feet: ")
        inches = ask_number("Height - inches: ", allow_zero=True)
        return pounds * KG_PER_POUND, (feet * 12 + inches) * METRES_PER_INCH

    kg = ask_number("Weight in kg: ")
    cm = ask_number("Height in cm: ")
    if cm < 3:   # someone probably typed 1.75 (metres) instead of 175 (cm)
        print("  That looks like metres, so I'll convert it to cm for you.")
        cm *= 100
    return kg, cm / 100


def main():
    print("=== BMI Calculator ===")
    weight_kg, height_m = get_measurements()
    bmi = calculate_bmi(weight_kg, height_m)
    print(f"\n  Your BMI is {bmi:.1f} ({bmi_category(bmi)})")


if __name__ == "__main__":
    main()
