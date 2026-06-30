import pandas as pd
import numpy as np

# DELIBERATELY MESSY DATA: np.nan represents a missing value.
# Real datasets almost always have gaps like this, someone forgot
# Eg: to fill in a field, a sensor failed, a survey question was skipped.
students = pd.DataFrame({
    "name": ["Gaurav", "Alice", "Bob", "Diana", "Eve", "Frank"],
    "age": [21, np.nan, 20, 23, 21, np.nan],
    "city": ["Kathmandu", "Pokhara", np.nan, "Butwal", "Biratnagar", "Pokhara"],
    "score": [88, 92, 75, np.nan, 81, 70]
})
print(f"Messy DataFrame:\n{students}\n")

# .isna() returns True wherever a value is missing, this is the
# detection step, always run this FIRST before deciding what to do
print(f"Null mask:\n{students.isna()}\n")

# .isna().sum() collapses that into a per-column count, the
# fastest way to see HOW MANY gaps exist in each column at a glance
print(f"Null count per column:\n{students.isna().sum()}\n")

# .any() tells us if ANY row has at least one missing value at all
print(f"Does any row have a null? {students.isna().any().any()}\n")

# DROPPING NULLS: .dropna() removes any ROW that has at least
# one missing value, by default. This is the simplest fix, but
# it can throw away good data just because ONE column was empty.
dropped = students.dropna()
print(f"After dropna() (default, drops any row with a null):\n{dropped}\n")

# dropna(subset=...) only checks specific columns, more targeted,
# we keep rows even if OTHER columns have gaps, just not this one
dropped_subset = students.dropna(subset=["score"])
print(f"After dropna(subset=['score']):\n{dropped_subset}\n")

# FILLING NULLS: usually smarter than dropping, since we keep
# the row instead of losing it entirely. The strategy matters,
# filling with the wrong value can quietly corrupt our analysis.
filled_zero = students.fillna(0)
print(f"Filled with 0 (often misleading for age/score):\n{filled_zero}\n")

# A BETTER STRATEGY: fill numeric columns with their mean, this
# keeps the column's overall average roughly intact instead of
# dragging it down artificially with zeros
age_mean = students["age"].mean()
score_mean = students["score"].mean()

students_filled = students.copy()
students_filled["age"] = students_filled["age"].fillna(age_mean)
students_filled["score"] = students_filled["score"].fillna(score_mean)
students_filled["city"] = students_filled["city"].fillna("Unknown")

print(f"Age filled with mean ({age_mean:.1f}), score filled with mean ({score_mean:.1f}), city filled with 'Unknown':\n{students_filled}")