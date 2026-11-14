"""
02 - Rock Paper Scissors
========================
Play against the computer. First to 3 wins takes the match.

Concepts you'll practise:
  - Lists and dictionaries
  - Using a dictionary as a RULE TABLE instead of lots of if-statements
  - Functions that return a value
  - Keeping score in a dictionary

Run:  python 02_rock_paper_scissors.py

Challenges:
  1. Add "lizard" and "spock" (look up the rules). Notice how little code changes!
  2. Let the player choose how many wins are needed.
  3. Make the computer pick whatever beats the player's most common move.
"""
import random

CHOICES = ["rock", "paper", "scissors"]
SHORTCUTS = {"r": "rock", "p": "paper", "s": "scissors"}

# Rule table: each key BEATS its value.
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

WINS_NEEDED = 3


def get_player_choice():
    """Return 'rock', 'paper', 'scissors' or 'quit'."""
    while True:
        text = input("Your move: (r)ock, (p)aper, (s)cissors or (q)uit: ").strip().lower()
        if text in ("q", "quit"):
            return "quit"
        # .get(key, default): turns 'r' into 'rock', leaves 'rock' as it is
        text = SHORTCUTS.get(text, text)
        if text in CHOICES:
            return text
        print("  Sorry, I didn't understand that.")


def decide_winner(player, computer):
    """Return 'player', 'computer' or 'tie'."""
    if player == computer:
        return "tie"
    if BEATS[player] == computer:
        return "player"
    return "computer"


def main():
    print("=== Rock Paper Scissors ===")
    print(f"First to {WINS_NEEDED} wins.\n")
    score = {"player": 0, "computer": 0, "tie": 0}

    while score["player"] < WINS_NEEDED and score["computer"] < WINS_NEEDED:
        player = get_player_choice()
        if player == "quit":
            print("Match abandoned.")
            return

        computer = random.choice(CHOICES)
        result = decide_winner(player, computer)
        score[result] += 1      # the result string doubles as the dictionary key

        print(f"  You: {player:<9} Computer: {computer}")
        if result == "tie":
            print("  It's a tie.")
        elif result == "player":
            print(f"  {player.capitalize()} beats {computer}. You win this round!")
        else:
            print(f"  {computer.capitalize()} beats {player}. Computer wins this round.")
        print(f"  Score: You {score['player']} - {score['computer']} Computer"
              f"  (ties: {score['tie']})\n")

    if score["player"] == WINS_NEEDED:
        print("You won the match!")
    else:
        print("The computer won the match. Better luck next time!")


if __name__ == "__main__":
    main()
