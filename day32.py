import pandas as pd
import numpy as np

students = pd.DataFrame({
    "name":  ["Gaurav", "Aaryan", "Biyanka", "Diana", "Evren"],
    "age":   [21, 22, 20, 23, 21],
    "city":  ["Kathmandu", "Pokhara", "Dhangadhi", "Butwal", "Rimuru"],
    "score": [88, 92, 75, 95, 81]
})
print(f"DataFrame:\n{students}\n")

# .apply() is the Pandas version of Day 10's map() and lambda
# same idea, apply a function to every element, but now on a
# DataFrame column (a Series) instead of a plain Python list.
# WHY THIS MATTERS: when vectorized operations aren't enough and
# we need custom logic per row, .apply() is the tool we reach for.

# PART 1: applying a lambda to a single column
# convert scores to a letter grade, can't do this with simple math
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "F"

# apply runs get_grade on every value in the score column
students["grade"] = students["score"].apply(get_grade)
print(f"After adding grade column:\n{students}\n")

# same thing using a lambda, more concise for simple conditions
students["passed"] = students["score"].apply(lambda x: "Pass" if x >= 75 else "Fail")
print(f"After adding passed column:\n{students}\n")

# PART 2: apply across multiple columns using axis=1
# axis=1 means apply runs on each ROW as a Series, not each column.
# This is how we combine values from multiple columns into one result.
# WHY THIS MATTERS: we often need to derive a new column from
# two or more existing ones together, not just one in isolation.
def performance_tag(row):
    if row["score"] >= 90 and row["age"] <= 21:
        return "Young Achiever"
    elif row["score"] >= 85:
        return "High Performer"
    else:
        return "On Track"

students["tag"] = students.apply(performance_tag, axis=1)
print(f"After adding performance tag:\n{students}\n")

# PART 3: apply a lambda with axis=1 for quick row-wise math
# create a "score-to-age ratio" — a made-up but illustrative metric
students["score_per_age"] = students.apply(
    lambda row: round(row["score"] / row["age"], 2), axis=1
)
print(f"After adding score per age ratio:\n{students}\n")

# PART 4: applying to string columns
# .str methods (Day 29) handle simple string ops cleanly, but for
# complex custom string logic, .apply() with a lambda is the answer
students["short_city"] = students["city"].apply(lambda x: x[:3].upper())
print(f"City abbreviations:\n{students[['name', 'city', 'short_city']]}\n")

# PART 5: apply vs vectorized operations
# apply() is flexible but SLOWER than direct vectorized operations
# because it loops under the hood. For simple math, prefer direct:
students["score_boosted"] = students["score"] + 5       # fast, vectorized
students["score_boosted2"] = students["score"].apply(lambda x: x + 5)  # slower, same result
print(f"Both methods give same result: {(students['score_boosted'] == students['score_boosted2']).all()}")
print(f"\nFinal DataFrame:\n{students}")