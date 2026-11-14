"""
05 - Currency Converter
=======================
Convert between currencies using a table of exchange rates.

IMPORTANT: the rates below are SAMPLE numbers for practice, not live market rates.

Concepts you'll practise:
  - A dictionary as a rate table
  - The same "convert to a base, then to the target" idea as project 04 (base = USD)
  - Number formatting with thousands separators: f"{x:,.2f}" -> 1,234,567.89
  - Cleaning user input: .strip().upper()

Run:  python 05_currency_converter.py

Challenges:
  1. Let the user add or update a rate from the menu.
  2. Save the rates to a JSON file so updates are remembered (you'll learn JSON in 09).
  3. Advanced: fetch live rates from a free exchange-rate API using the
     requests library (pip install requests). Search "free exchange rate API".
"""

# How many units of each currency equal 1 US dollar. SAMPLE VALUES ONLY.
RATES_PER_USD = {
    "USD": 1.0,
    "SGD": 1.30,
    "MYR": 4.20,
    "IDR": 16000.0,
    "THB": 33.0,
    "VND": 25000.0,
    "PHP": 58.0,
    "EUR": 0.92,
    "GBP": 0.78,
    "JPY": 150.0,
    "AUD": 1.50,
    "INR": 84.0,
}


def convert(amount, from_code, to_code):
    amount_in_usd = amount / RATES_PER_USD[from_code]
    return amount_in_usd * RATES_PER_USD[to_code]


def ask_amount():
    while True:
        text = input("Amount: ").replace(",", "").strip()   # allow "1,000"
        try:
            amount = float(text)
        except ValueError:
            print("  Please enter a number.")
            continue
        if amount >= 0:
            return amount
        print("  Amount can't be negative.")


def ask_currency(prompt):
    while True:
        code = input(f"{prompt} currency code: ").strip().upper()
        if code in RATES_PER_USD:
            return code
        print(f"  Unknown code. Options: {', '.join(RATES_PER_USD)}")


def show_rates():
    print("\n  Sample rates (1 USD = ...)")
    for code, rate in RATES_PER_USD.items():
        print(f"    {code}  {rate:>12,.2f}")


def main():
    print("=== Currency Converter ===")
    print("(Practice rates only - not live market data)")
    while True:
        print("\n  1. Convert\n  2. Show rate table\n  0. Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            amount = ask_amount()
            from_code = ask_currency("From")
            to_code = ask_currency("To")
            result = convert(amount, from_code, to_code)
            one_unit = convert(1, from_code, to_code)
            print(f"\n  {amount:,.2f} {from_code} = {result:,.2f} {to_code}")
            print(f"  (1 {from_code} = {one_unit:,.4f} {to_code})")
        elif choice == "2":
            show_rates()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("  Please choose 1, 2 or 0.")


if __name__ == "__main__":
    main()
