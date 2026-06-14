import datetime

now = datetime.datetime.now()

# WRITE — create a fresh file
with open("learning_log.txt", "w") as f:
    f.write(f"Learning Log — {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 40 + "\n")

# APPEND — add entries one by one without overwriting
days = [
    "Day 1  : Variables & I/O",
    "Day 2  : Conditionals",
    "Day 3  : Lists",
    "Day 4  : Tuples & Loops",
    "Day 5  : Dicts & Sets",
    "Day 6  : Comprehensions",
    "Day 7  : While Loops",
    "Day 8  : Functions I",
    "Day 9  : Functions II",
    "Day 10 : Lambda, map, filter",
    "Day 11 : Exception Handling",
    "Day 12 : OS & Datetime",
    "Day 13 : File I/O",
]

for entry in days:
    with open("learning_log.txt", "a") as f:
        f.write(entry + "\n")

# READ — load the whole file back
print("📄 Learning Log:\n")
with open("learning_log.txt", "r") as f:
    print(f.read())