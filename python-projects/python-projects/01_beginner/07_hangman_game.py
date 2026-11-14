"""
07 - Hangman
============
Guess the hidden word one letter at a time before the drawing is complete.

Concepts you'll practise:
  - Sets: perfect for "letters already guessed" (no duplicates, fast lookups)
  - Set maths: set(word) <= guessed means "every letter of the word was guessed"
  - Building a string with a generator expression and " ".join(...)
  - A list of multi-line strings (ASCII art), picked by index
  - Raw strings r"..." so backslashes in the drawing aren't treated as escapes

Run:  python 07_hangman_game.py

Challenges:
  1. Add categories (animals, countries, ...) the player can choose from.
  2. Let the player guess the whole word at once.
  3. Load the words from a text file instead of the list below.
"""
import random

WORDS = [
    "python", "variable", "function", "dictionary", "loop", "string",
    "integer", "keyboard", "program", "boolean", "pipeline", "algorithm",
    "database", "terminal", "notebook", "github", "debugging", "syntax",
]

STAGES = [
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]
MAX_WRONG = len(STAGES) - 1     # 6 wrong guesses allowed


def masked_word(word, guessed):
    """'python' with guessed {'p','o'} -> 'p _ _ _ o _'"""
    return " ".join(letter if letter in guessed else "_" for letter in word)


def play():
    word = random.choice(WORDS)
    guessed = set()
    wrong = 0

    while True:
        print(STAGES[wrong])
        print("Word:  ", masked_word(word, guessed))
        wrong_letters = sorted(guessed - set(word))     # letters guessed but NOT in the word
        print("Missed:", " ".join(wrong_letters) or "-")

        if set(word) <= guessed:
            print("\nYou won!")
            return True
        if wrong >= MAX_WRONG:
            print(f"\nYou lost! The word was '{word}'.")
            return False

        guess = input("\nGuess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("  Please enter a single letter.")
            continue
        if guess in guessed:
            print("  You already tried that one.")
            continue

        guessed.add(guess)
        if guess not in word:
            wrong += 1


def main():
    print("=== Hangman ===")
    wins = losses = 0
    while True:
        if play():
            wins += 1
        else:
            losses += 1
        print(f"Wins: {wins}  Losses: {losses}")
        if input("Play again? (y/n): ").strip().lower() != "y":
            break


if __name__ == "__main__":
    main()
