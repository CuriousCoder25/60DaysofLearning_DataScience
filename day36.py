import pandas as pd
import numpy as np

# THREE MONTHLY EXAM RESULT FILES : same columns, different time periods.
# This is the most common real-world concat scenario: you have the same
# kind of data arriving in chunks (monthly reports, weekly logs, daily
# sensor readings) and need to stack them into one unified dataset.
april = pd.DataFrame({
    "student_id": [1, 2, 3],
    "name":       ["Gaurav", "Alice", "Pino"],
    "score":      [88, 92, 75],
    "month":      ["April", "April", "April"]
})

may = pd.DataFrame({
    "student_id": [1, 2, 3],
    "name":       ["Gaurav", "Alice", "Pino"],
    "score":      [91, 88, 80],
    "month":      ["May", "May", "May"]
})

june = pd.DataFrame({
    "student_id": [1, 2, 3],
    "name":       ["Gaurav", "Alice", "Pino"],
    "score":      [85, 95, 83],
    "month":      ["June", "June", "June"]
})

print(f"April:\n{april}\n")
print(f"May:\n{may}\n")
print(f"June:\n{june}\n")

# pd.concat() stacks DataFrames along an axis.
# axis=0 (default) = stack VERTICALLY, adding more rows.
# This connects directly to Day 24's np.vstack(), same concept
# but now on labeled DataFrames instead of raw arrays.
all_months = pd.concat([april, may, june], axis=0)
print(f"After concat (axis=0):\n{all_months}\n")

# NOTICE: the index repeats 0,1,2 three times because each
# monthly DataFrame brought its own index along. This is a
# very common source of bugs when filtering or slicing later.
print(f"Index after concat: {list(all_months.index)}\n")

# ignore_index=True resets the index to a clean 0,1,2...N sequence.
# WHY THIS MATTERS: duplicate index values cause subtle bugs in
# .loc[] and .groupby() operations downstream, always reset after concat.
all_months_clean = pd.concat([april, may, june], axis=0, ignore_index=True)
print(f"After concat with ignore_index=True:\n{all_months_clean}\n")
print(f"Index now clean: {list(all_months_clean.index)}\n")

# keys= adds a hierarchical MultiIndex so we can still tell which
# rows came from which original DataFrame after stacking.
# useful when we need to track data provenance (where did this row come from?)
all_months_keyed = pd.concat(
    [april, may, june],
    keys=["april", "may", "june"]
)
print(f"With keys (MultiIndex):\n{all_months_keyed}\n")

# HORIZONTAL CONCAT: axis=1 stacks DataFrames SIDE BY SIDE,
# same as Day 24's np.hstack(), adds more columns instead of more rows.
# Both DataFrames must share the same index for this to align correctly.
scores_only = pd.DataFrame({
    "math":    [88, 92, 75],
    "science": [90, 85, 78]
})
extra_info = pd.DataFrame({
    "grade": ["B", "A", "C"],
    "passed": [True, True, False]
})

side_by_side = pd.concat([scores_only, extra_info], axis=1)
print(f"Horizontal concat (axis=1):\n{side_by_side}\n")

# PRACTICAL ANALYSIS on the stacked monthly data:
# now that all months are in one table, we can ask questions
# that span the entire period with simple groupby operations.

# Q1: how did each student's score trend across months?
# sort by student and month to see progression clearly
trend = all_months_clean.sort_values(["student_id", "month"])
print(f"Score trend per student:\n{trend}\n")

# Q2: which month had the highest average score overall?
month_avg = all_months_clean.groupby("month")["score"].mean().sort_values(ascending=False)
print(f"Average score per month:\n{month_avg}\n")

# Q3: who improved the most from April to June?
april_scores = april.set_index("name")["score"]
june_scores  = june.set_index("name")["score"]
improvement  = (june_scores - april_scores).sort_values(ascending=False)
print(f"Improvement from April to June:\n{improvement}\n")
print(f"Most improved: {improvement.idxmax()} (+{improvement.max()} points)")