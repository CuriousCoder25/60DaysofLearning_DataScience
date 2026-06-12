# 1. Basic try/except — instead of crashing, catch the error gracefully
result = None
try:
    result = 10 / 0   # this will blow up without a try block
except ZeroDivisionError as e:
    print(f"Caught it: {e}")   # handle it, don't crash

# 2. Multiple except blocks — different errors, different responses
def parse_score(value):
    try:
        score = int(value)      # might fail if value isn't a number
        result = 100 / score    # might fail if score is 0
        return result
    except ValueError:
        print(f"'{value}' isn't a valid number")
    except ZeroDivisionError:
        print("Score can't be zero")

parse_score("abc")   # triggers ValueError
parse_score(0)       # triggers ZeroDivisionError
parse_score(25)      # works fine

# 3. finally — runs NO MATTER WHAT, even if an error occurred
# useful for cleanup — closing files, db connections etc.
def read_data(filename):
    try:
        file = open(filename, "r")
        data = file.read()
        return data
    except FileNotFoundError:
        print(f"'{filename}' doesn't exist")
    finally:
        print("Attempted file read — moving on")  # always runs

read_data("missing.txt")

# 4. raise — manually trigger an error when data looks wrong
# useful for validating inputs before they cause silent bugs downstream
def set_age(age):
    if age < 0 or age > 120:
        raise ValueError(f"Age {age} is out of range — expected 0–120")
    return f"Age set to {age}"

try:
    print(set_age(150))   # should fail our custom check
except ValueError as e:
    print(f"Validation error: {e}")