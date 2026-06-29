import pandas as pd

students = pd.DataFrame({
    "name": ["Gaurav", "Alice", "Bob", "Diana", "Eve"],
    "age": [21, 22, 20, 23, 21],
    "city": ["Kathmandu", "Pokhara", "Dhangadhi", "Butwal", "Biratnagar"],
    "score": [88, 92, 75, 95, 81]
})
print(f"DataFrame:\n{students}\n")

# THE CORE IDEA: this is Day 19's NumPy boolean masking applied
# to a DataFrame instead of a raw array. students["score"] > 85
# returns True/False for every row, then we use that to filter.
mask = students["score"] > 85
print(f"Mask (score > 85):\n{mask}\n")

high_scorers = students[mask]
print(f"High scorers:\n{high_scorers}\n")

# Same thing in one line, the actual pattern used in real code
print(f"Same, inline:\n{students[students['score'] > 85]}\n")

# COMBINING CONDITIONS: use & for AND, | for OR, just like NumPy.
# Each condition needs its own parentheses, this is a common
# bug source if forgotten, Python will throw a confusing error.
young_high_scorers = students[(students["age"] < 22) & (students["score"] > 80)]
print(f"Young and high scoring:\n{young_high_scorers}\n")

# OR condition: either very young or very high scoring
either_condition = students[(students["age"] < 21) | (students["score"] > 90)]
print(f"Very young OR very high score:\n{either_condition}\n")

# FILTERING BY TEXT: .str accessor lets us run string methods
# on an entire column at once, no loop needed.
kathmandu_students = students[students["city"].str.contains("mandu")]
print(f"Cities containing 'mandu':\n{kathmandu_students}\n")

# .isin() checks membership against a list, cleaner than chaining
# multiple OR conditions when checking several specific values
target_cities = ["Pokhara", "Butwal"]
selected = students[students["city"].isin(target_cities)]
print(f"Students from Pokhara or Butwal:\n{selected}\n")

# .query() IS THE READABLE ALTERNATIVE: same filtering logic,
# but written like a plain English condition instead of bracket
# syntax. Column names go in directly, no students[...] repeated.
queried = students.query("score > 85 and age < 23")
print(f"Using .query():\n{queried}\n")

# query() can also reference external variables with @
min_score = 90
top = students.query("score >= @min_score")
print(f"Using .query() with a variable:\n{top}")


# key point to understand: Boolean masking on a DataFrame works exactly like Day 19's NumPy masking, just
# applied to a column instead of a raw array. .query() does the same filtering, but reads like a sentence 
# instead of bracket syntax, which becomes genuinely valuable once conditions get longer and harder to read as nested brackets.