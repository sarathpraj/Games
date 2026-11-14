import random

choices = ["rock", "paper", "scissors"]
player_score = 0
computer_score = 0

print("Welcome to Rock, Paper, Scissors!")
print("First to 3 points wins!")

while player_score < 3 and computer_score < 3:
    print(f"\nScore - You: {player_score} | Computer: {computer_score}")
    
    player = input("Choose rock, paper, or scissors: ").lower()
    
    if player not in choices:
        print("Invalid choice. Try again.")
        continue
        
    computer = random.choice(choices)
    print(f"Computer chose: {computer}")
    
    if player == computer:
        print("It's a tie!")
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        print("You win this round!")
        player_score += 1
    else:
        print("Computer wins this round!")
        computer_score += 1

print("\n--- Final Score ---")
print(f"You: {player_score} | Computer: {computer_score}")

if player_score == 3:
    print("Congratulations! You won the game!")
else:
    print("The computer won the game. Better luck next time!")