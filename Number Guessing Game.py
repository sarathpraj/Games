import random

secret_number = random.randint(1,10)
attempts = 0

print("Welcome to the number guessing game..!!")
print("I'm thinking of a number between 1 and 10.")

while True:
    guess = int(input("Take a guess: "))
    attempts += 1

    if guess < secret_number:
        print("Higher..!")
    elif guess > secret_number:
        print("Lower..!!")
    else:
        print(f"congratulations..!! You guessed the right number in {attempts} attempts")

        break