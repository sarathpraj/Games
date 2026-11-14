"""
08 - Tic-Tac-Toe
================
Play against a friend or against a simple computer opponent.

Concepts you'll practise:
  - Representing a 3x3 board as ONE list of 9 cells (index = row * 3 + col)
  - A list of tuples to describe every winning line
  - Tuple unpacking in loops: for a, b, c in WIN_LINES
  - "Try a move, check it, undo it" - the core idea behind most game AI
  - None as "empty"

Board positions:
   1 | 2 | 3
  ---+---+---
   4 | 5 | 6
  ---+---+---
   7 | 8 | 9

Run:  python 08_tic_tac_toe.py

Challenges:
  1. Let the human choose X or O, and who goes first.
  2. Make the computer unbeatable (look up the "minimax" algorithm).
  3. Add an "easy" mode where the computer just plays randomly.
"""
import random

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]


def print_board(board):
    print()
    for row in range(3):
        cells = []
        for col in range(3):
            i = row * 3 + col
            cells.append(board[i] if board[i] else str(i + 1))   # show number if empty
        print(f" {cells[0]} | {cells[1]} | {cells[2]}")
        if row < 2:
            print("---+---+---")
    print()


def get_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def empty_cells(board):
    return [i for i, cell in enumerate(board) if cell is None]


def human_move(board, mark):
    while True:
        text = input(f"Player {mark}, choose a square (1-9): ").strip()
        if text.isdigit() and 1 <= int(text) <= 9:
            i = int(text) - 1
            if board[i] is None:
                return i
            print("  That square is taken.")
        else:
            print("  Please type a number from 1 to 9.")


def find_winning_move(board, mark):
    """Return a square that wins immediately for `mark`, or None."""
    for i in empty_cells(board):
        board[i] = mark                  # try the move...
        won = get_winner(board) == mark
        board[i] = None                  # ...then undo it
        if won:
            return i
    return None


def computer_move(board, mark):
    opponent = "O" if mark == "X" else "X"
    move = find_winning_move(board, mark)              # 1. win if we can
    if move is None:
        move = find_winning_move(board, opponent)      # 2. block the opponent
    if move is None and board[4] is None:
        move = 4                                       # 3. take the centre
    if move is None:
        corners = [i for i in (0, 2, 6, 8) if board[i] is None]
        move = random.choice(corners) if corners else random.choice(empty_cells(board))
    return move


def play_game(vs_computer):
    board = [None] * 9
    current = "X"                        # X always starts (that's you)
    while True:
        print_board(board)
        if vs_computer and current == "O":
            move = computer_move(board, current)
            print(f"Computer plays {move + 1}")
        else:
            move = human_move(board, current)
        board[move] = current

        winner = get_winner(board)
        if winner:
            print_board(board)
            print(f"{winner} wins!")
            return winner
        if not empty_cells(board):
            print_board(board)
            print("It's a draw.")
            return "draw"
        current = "O" if current == "X" else "X"


def main():
    print("=== Tic-Tac-Toe ===")
    mode = input("1) Play vs computer   2) Two players : ").strip()
    vs_computer = mode != "2"
    scores = {"X": 0, "O": 0, "draw": 0}

    while True:
        result = play_game(vs_computer)
        scores[result] += 1
        print(f"Scores -> X: {scores['X']}  O: {scores['O']}  Draws: {scores['draw']}")
        if input("Play again? (y/n): ").strip().lower() != "y":
            break


if __name__ == "__main__":
    main()
