import random

# 1. Basic while loop
count = 1
while count <= 5:
    print(f"Count: {count}")
    count += 1

# 2. continue — skip odd numbers
print("\nEven numbers only:")
num = 0
while num < 10:
    num += 1
    if num % 2 != 0:
        continue
    print(num)

# 3. Number guessing game — uses while + break
print("\n Number Guessing Game:")
secret = random.randint(1, 10)
attempts = 0

while True:
    guess = int(input("Guess (1–10): "))
    attempts += 1

    if guess < secret:
        print("Too low!")
    elif guess > secret:
        print("Too high!")
    else:
        print(f"Correct! Got it in {attempts} attempts.")
        break