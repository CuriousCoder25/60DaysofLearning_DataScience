import pandas as pd
import numpy as np

# TWO SEPARATE TABLES sharing a common key "student_id".
# This is the realistic scenario: data about the same entities
# lives in different files/tables and we need to combine them.
# WHY THIS MATTERS: real data is almost never in one flat table.
# Sales data, customer data, product data all live separately
# and need to be joined before any analysis can happen.
students = pd.DataFrame({
    "student_id": [1, 2, 3, 4, 5],
    "name":       ["Gaurav", "Anuska", "Pino", "Diana", "Evren"],
    "city":       ["Kathmandu", "Pokhara", "Kathmandu", "Butwal", "Pokhara"]
})

scores = pd.DataFrame({
    "student_id": [1, 2, 3, 6, 7],    # note: 4 and 5 are missing, 6 and 7 are new
    "math":       [88, 92, 75, 85, 90],
    "science":    [90, 85, 78, 88, 76]
})

print(f"Students table:\n{students}\n")
print(f"Scores table:\n{scores}\n")

# INNER JOIN: keeps only rows where the key exists in BOTH tables.
# Students 4 and 5 have no scores, students 6 and 7 have no names.
# Inner join drops ALL of them, only 1, 2, 3 survive.
# WHY THIS MATTERS: use inner when we only want complete records,
# rows with data on both sides. Anything unmatched gets silently dropped.
inner = pd.merge(students, scores, on="student_id", how="inner")
print(f"Inner join (only matched rows):\n{inner}\n")

# LEFT JOIN: keeps ALL rows from the LEFT table (students),
# fills with NaN for any columns from the right table (scores)
# that have no matching key. Students 4 and 5 survive with NaN scores.
# Students 6 and 7 are still dropped because they're not in the left table.
# WHY THIS MATTERS: use left when the left table is our "master" list
# and we want to keep everyone in it, even if some have missing data.
left = pd.merge(students, scores, on="student_id", how="left")
print(f"Left join (all students, NaN if no scores):\n{left}\n")

# RIGHT JOIN: mirror of left, keeps ALL rows from the RIGHT table.
# Students 6 and 7 now survive with NaN names/cities.
# Students 4 and 5 are dropped because they're not in the right table.
right = pd.merge(students, scores, on="student_id", how="right")
print(f"Right join (all scores, NaN if no student info):\n{right}\n")

# OUTER JOIN: keeps EVERYTHING from both tables.
# Students 4 and 5 survive with NaN scores.
# Students 6 and 7 survive with NaN names/cities.
# No row is ever dropped, missing values filled with NaN.
# WHY THIS MATTERS: use outer when we want a complete picture of
# ALL entities across both tables, even if data is incomplete.
outer = pd.merge(students, scores, on="student_id", how="outer")
print(f"Outer join (everything, NaN where no match):\n{outer}\n")

# MERGING ON DIFFERENT COLUMN NAMES: real tables often use
# different names for the same key. left_on and right_on handle this.
scores_renamed = scores.rename(columns={"student_id": "id"})
merged_diff_keys = pd.merge(
    students, scores_renamed,
    left_on="student_id",   # key name in left table
    right_on="id",          # key name in right table
    how="inner"
)
print(f"Merged with different key names:\n{merged_diff_keys}\n")

# PRACTICAL PATTERN: after a left join, check how many rows
# got NaN scores, this tells us how many students have no score data.
# isnull().sum() counts NaN values per column, same as Day 30's isna().
missing_scores = left[left["math"].isnull()]
print(f"Students with no score data:\n{missing_scores}\n")

# THE MERGE SUMMARY TO REMEMBER:
summary = pd.DataFrame({
    "join_type": ["inner", "left", "right", "outer"],
    "keeps":     [
        "only matched rows from both",
        "all left rows, matched right",
        "all right rows, matched left",
        "everything from both sides"
    ],
    "drops": [
        "unmatched rows from either side",
        "unmatched right rows only",
        "unmatched left rows only",
        "nothing, NaN fills gaps"
    ]
})
print(f"Join type summary:\n{summary}")