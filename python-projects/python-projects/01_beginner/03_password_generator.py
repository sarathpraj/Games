"""
03 - Password Generator
=======================
Creates strong random passwords based on the options you choose.

Concepts you'll practise:
  - The string module: ready-made sets of letters, digits and symbols
  - The secrets module: the RIGHT way to make random values for security.
    (random is fine for games, but it is predictable. Never use it for passwords.)
  - Building a string from a list with "".join(...)
  - Small helper functions for validated input, with default values

Run:  python 03_password_generator.py

Challenges:
  1. Add an option to leave out look-alike characters (O/0, l/1/I).
  2. Rate each password as weak / medium / strong.
  3. Copy the chosen password to the clipboard (look up the pyperclip library).
"""
import secrets
import string

MIN_LENGTH = 8


def ask_yes_no(question, default=True):
    hint = "Y/n" if default else "y/N"
    answer = input(f"{question} [{hint}]: ").strip().lower()
    if not answer:              # user just pressed Enter
        return default
    return answer.startswith("y")


def ask_length(default=16):
    while True:
        text = input(f"Password length [{default}]: ").strip()
        if not text:
            return default
        if text.isdigit() and int(text) >= MIN_LENGTH:
            return int(text)
        print(f"  Please enter a whole number of at least {MIN_LENGTH}.")


def generate_password(length, use_upper=True, use_digits=True, use_symbols=True):
    pools = [string.ascii_lowercase]            # always include a-z
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(string.punctuation)

    # 1) Guarantee at least one character from every pool the user chose
    chars = [secrets.choice(pool) for pool in pools]

    # 2) Fill the rest from all allowed characters combined
    all_allowed = "".join(pools)
    while len(chars) < length:
        chars.append(secrets.choice(all_allowed))

    # 3) Shuffle so the guaranteed characters aren't always at the start
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def main():
    print("=== Password Generator ===")
    length = ask_length()
    use_upper = ask_yes_no("Include UPPERCASE letters?")
    use_digits = ask_yes_no("Include numbers?")
    use_symbols = ask_yes_no("Include symbols (!@#...)?")

    print("\nHere are 3 options. Pick the one you like:")
    for i in range(1, 4):
        print(f"  {i}. {generate_password(length, use_upper, use_digits, use_symbols)}")


if __name__ == "__main__":
    main()
