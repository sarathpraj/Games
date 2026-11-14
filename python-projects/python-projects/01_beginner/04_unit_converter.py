"""
04 - Unit Converter
===================
Convert length, weight, volume and temperature.

Concepts you'll practise:
  - Nested dictionaries as lookup tables
  - The "convert to a BASE unit, then to the target" pattern.
    This keeps the table small: 8 units need 8 numbers, not 8 x 8 = 64.
  - Why temperature needs its own function (it has an offset, not just a multiplier)
  - A menu driven by a while loop

Run:  python 04_unit_converter.py

Challenges:
  1. Add an "Area" category (m2, ft2, acre, hectare). You only edit the dictionary!
  2. Let the user type "5 km to mi" on one line (hint: text.split()).
  3. Show the value converted into EVERY unit of the category at once.
"""

# For each category: how many BASE units one of each unit is worth.
# Base units are: metre (length), kilogram (weight), litre (volume).
LINEAR_UNITS = {
    "Length": {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
               "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344},
    "Weight": {"mg": 0.000001, "g": 0.001, "kg": 1.0, "t": 1000.0,
               "oz": 0.028349523125, "lb": 0.45359237},
    "Volume": {"ml": 0.001, "l": 1.0, "tsp": 0.00492892, "tbsp": 0.0147868,
               "cup": 0.236588, "gal": 3.785411784},
}
TEMPERATURE_UNITS = ["c", "f", "k"]
MENU = list(LINEAR_UNITS) + ["Temperature"]   # ['Length', 'Weight', 'Volume', 'Temperature']


def convert_linear(value, from_unit, to_unit, factors):
    in_base = value * factors[from_unit]      # e.g. 5 km -> 5000 m
    return in_base / factors[to_unit]         # e.g. 5000 m -> 3.107 mi


def convert_temperature(value, from_unit, to_unit):
    # Step 1: whatever we have -> Celsius
    if from_unit == "c":
        celsius = value
    elif from_unit == "f":
        celsius = (value - 32) * 5 / 9
    else:  # "k"
        celsius = value - 273.15
    # Step 2: Celsius -> whatever we want
    if to_unit == "c":
        return celsius
    if to_unit == "f":
        return celsius * 9 / 5 + 32
    return celsius + 273.15


def pretty(number):
    """Format a number nicely: 1,000 instead of 1000.0000, and tiny numbers as 1.0e-06."""
    if number != 0 and abs(number) < 0.001:
        return f"{number:.3e}"
    return f"{number:,.4f}".rstrip("0").rstrip(".")


def ask_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Please enter a number.")


def ask_unit(prompt, valid_units):
    while True:
        unit = input(f"{prompt} ({', '.join(valid_units)}): ").strip().lower()
        if unit in valid_units:
            return unit
        print("  Unknown unit, try again.")


def main():
    print("=== Unit Converter ===")
    while True:
        print("\nWhat do you want to convert?")
        for i, name in enumerate(MENU, start=1):
            print(f"  {i}. {name}")
        print("  0. Quit")

        choice = input("Choose: ").strip()
        if choice == "0":
            print("Bye!")
            break
        if not choice.isdigit() or not 1 <= int(choice) <= len(MENU):
            print("  Please pick a number from the menu.")
            continue

        category = MENU[int(choice) - 1]
        value = ask_number("Value: ")

        if category == "Temperature":
            from_unit = ask_unit("From", TEMPERATURE_UNITS)
            to_unit = ask_unit("To", TEMPERATURE_UNITS)
            result = convert_temperature(value, from_unit, to_unit)
        else:
            factors = LINEAR_UNITS[category]
            from_unit = ask_unit("From", list(factors))
            to_unit = ask_unit("To", list(factors))
            result = convert_linear(value, from_unit, to_unit, factors)

        print(f"\n  {pretty(value)} {from_unit} = {pretty(result)} {to_unit}")


if __name__ == "__main__":
    main()
