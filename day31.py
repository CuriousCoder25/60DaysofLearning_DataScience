import pandas as pd
import numpy as np

# Working on DELIBERATELY MESSY DATA: real datasets come with duplicates, inconsistent casing, 
# wrong types, and whitespace everywhere.
# This is what a raw CSV actually looks like before cleaning.
students = pd.DataFrame({
    "name":  ["Gaurav", "Alice", "Bob", "Diana", "Eve", "gaurav", "ALICE", "Bob"],
    "age":   [21, 22, 20, 23, 21, 21, 22, 20],
    "city":  ["Kathmandu", "Pokhara", "Dhangadhi", "Butwal", "Biratnagar", "kathmandu", "POKHARA", "Dhangadhi"],
    "score": ["88", "92", "75", "95", "81", "88", "92", "75"]  # scores as STRINGS, common CSV issue
})
print(f"Messy DataFrame:\n{students}\n")

# CHECKING TYPES FIRST: always inspect dtypes before doing any
# math or comparison, "88" as a string and 88 as an int look
# identical when printed but behave completely differently in code.
print(f"Column types (before cleaning):\n{students.dtypes}\n")

# WHY THIS MATTERS: try averaging the score column right now
# and it fails or gives wrong results because it's a string column.
# This is a silent bug that corrupts analysis without always erroring.
try:
    print(students["score"].mean())
except TypeError as e:
    print(f"Can't average a string column: {e}\n")

# FIX 1: convert score from string to integer using astype()
# astype() is the Pandas version of Python's int() / float()
# but applied across the entire column at once, no loop needed.
students["score"] = students["score"].astype(int)
print(f"Score column after astype(int): {students['score'].values}")
print(f"Mean score now works: {students['score'].mean()}\n")

# FIX 2: normalize string columns so "gaurav", "Gaurav", "GAURAV"
# all become the same value before we check for duplicates.
# .str accessor works on the whole column at once, same idea
# as Day 29's .str.contains(), just a different string method.
students["name"] = students["name"].str.strip().str.title()
students["city"] = students["city"].str.strip().str.title()
print(f"After string normalization:\n{students}\n")

# FINDING DUPLICATES: .duplicated() returns True for every row
# that is an exact copy of a row that appeared earlier.
# keep='first' means the FIRST occurrence is kept, rest flagged.
print(f"Duplicate rows:\n{students[students.duplicated()]}\n")

# DROP DUPLICATES: removes all flagged duplicate rows, keeping
# the first occurrence of each. This is why we normalized strings
# FIRST, without that step "gaurav" and "Gaurav" wouldn't be
# caught as duplicates since they look different to the computer.
cleaned = students.drop_duplicates()
print(f"After drop_duplicates():\n{cleaned}\n")

# drop_duplicates on a SUBSET of columns, useful when we only
# care about uniqueness within specific fields, not the whole row.
# here: keep only one row per unique name, regardless of other cols
unique_names = students.drop_duplicates(subset=["name"])
print(f"Unique by name only:\n{unique_names}\n")

# FINAL CHECK: confirm types are all correct after cleaning
print(f"Column types (after cleaning):\n{cleaned.dtypes}")