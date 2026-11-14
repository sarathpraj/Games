"""
01 - Number Guessing Game
=========================
The computer picks a secret number. You keep guessing until you find it.

Concepts you'll practise:
  - import and the random module
  - while loops (repeat until something happens)
  - input() always returns TEXT, so we convert it with int()
  - try / except to handle bad input without crashing
  - if / elif / else

Run:  python 01_number_guessing_game.py

Challenges (do at least one!):
  1. Add difficulty levels: easy (1-10), medium (1-100), hard (1-1000).
  2. Limit the player to 7 guesses.
  3. Remember the best (lowest) score across rounds.
"""
import random


def get_guess(low, high):
    """Keep asking until the user types a whole number between low and high."""
    while True:
        text = input(f"Guess a number between {low} and {high}: ")
        try:
            guess = int(text)          # "42" -> 42. "abc" -> ValueError
        except ValueError:
            print("  That's not a whole number. Try again.")
            continue                   # jump back to the top of the loop
        if low <= guess <= high:
            return guess
        print(f"  Please stay between {low} and {high}.")


def play_round(low=1, high=100):
    """Play one round. Returns how many guesses it took."""
    secret = random.randint(low, high)  # includes both low and high
    attempts = 0

    while True:
        guess = get_guess(low, high)
        attempts += 1                   # same as: attempts = attempts + 1

        if guess < secret:
            print("  Too low!")
        elif guess > secret:
            print("  Too high!")
        else:
            print(f"  Correct! It was {secret}. You needed {attempts} guesses.")
            return attempts


def main():
    print("=== Number Guessing Game ===")
    while True:
        play_round()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


# This line means: only run main() when this file is run directly,
# not when another file imports it. You'll see it in every project.
if __name__ == "__main__":
    main()
