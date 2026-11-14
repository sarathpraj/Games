import string
import secrets

print("=== Password Generator ===")

# Ask the user for password length
length = int(input("Enter password length: "))

# Characters that can be used in the password
characters = string.ascii_letters + string.digits + string.punctuation

print("\nHere are 3 generated passwords:")

# Generate 3 passwords
for i in range(3):
    password = "".join(
        secrets.choice(characters) for _ in range(length)
    )

    print(f"{i + 1}. {password}")   