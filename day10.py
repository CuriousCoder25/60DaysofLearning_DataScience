# 1. Regular function vs lambda — same thing, different syntax
# normal way
def square(x):
    return x ** 2

# lambda way — no name, one line, one expression
square_l = lambda x: x ** 2

print(square(5))    # 25
print(square_l(5))  # same result, less code

# 2. map() — apply a function to every item in a list
# instead of looping and appending manually, map does it for you
scores = [55, 72, 88, 91, 63]

# bump every score up by 5 — map returns a map object, wrap in list()
curved = list(map(lambda x: x + 5, scores))
print(f"Original : {scores}")
print(f"Curved   : {curved}")

# 3. filter() — keep only items that pass a condition
# only returns items where the lambda returns True
passing = list(filter(lambda x: x >= 70, curved))
print(f"Passing scores (>=70): {passing}")

# 4. chaining map + filter together — this is where it gets useful
# real pattern: clean raw data, then filter it in one go
raw_names = ["  gaurav  ", "ALICE", " bob ", "Diana  "]

# step 1 — map