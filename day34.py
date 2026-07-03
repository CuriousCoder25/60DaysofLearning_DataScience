import pandas as pd
import numpy as np

students = pd.DataFrame({
    "name":    ["Gaurav", "Alice", "Pino", "Diana", "Evren"],
    "city":    ["Kathmandu", "Pokhara", "Kathmandu", "Butwal", "Pokhara"],
    "math":    [88, 92, 75, 95, 81],
    "science": [90, 85, 78, 88, 76],
    "english": [78, 95, 80, 91, 83]
})
print(f"Wide format (original):\n{students}\n")

# pivot_table() summarizes data into a cross-tabulation.
# index= sets what becomes the row labels (cities here).
# values= sets which columns to aggregate (our three subjects).
# aggfunc= sets HOW to aggregate, mean/sum/count/max/min all work.
# WHY THIS MATTERS: answers "how did each city perform per subject?"
# in one line instead of three separate groupby operations.
pivot = students.pivot_table(
    values=["math", "science", "english"],
    index="city",
    aggfunc="mean"
)
print(f"Pivot table (city vs subject averages):\n{pivot}\n")

pivot_count = students.pivot_table(
    values="math",
    index="city",
    aggfunc="count"
)
print(f"Student count per city:\n{pivot_count}\n")

# melt() is the OPPOSITE of pivot_table.
# it converts WIDE format (one row per student, one column per subject)
# into LONG format (one row per student-subject combination).
# id_vars= are the columns we keep as identifiers, they repeat per row.
# value_vars= are the columns we collapse into one unified column.
# var_name= names the new column that holds the old column headers.
# value_name= names the new column that holds the actual measurements.
# WHY THIS MATTERS: ML models and Seaborn prefer long format because
# every observation is its own row, one thing measured once per row.
long_format = students.melt(
    id_vars=["name", "city"],
    value_vars=["math", "science", "english"],
    var_name="subject",
    value_name="score"
)
print(f"Long format (after melt):\n{long_format}\n")

# THE KEY DIFFERENCE TO REMEMBER:
# Wide: 5 rows (one per student), 5 columns
# Long: 15 rows (one per student-subject pair), 4 columns
print(f"Wide shape : {students.shape}")
print(f"Long shape : {long_format.shape}\n")

# reset_index() moves the index back into regular columns.
# after pivot_table, "name" and "city" become the index (row labels),
# not regular columns we can filter or groupby on. reset_index()
# pushes them back into the DataFrame as normal columns.
# WHY THIS MATTERS: without it, the result looks clean but behaves
# strangely when we try to access those columns normally.
wide_again = long_format.pivot_table(
    values="score",
    index=["name", "city"],
    columns="subject",
    aggfunc="mean"
).reset_index()
print(f"Back to wide format:\n{wide_again}\n")

# ---- WHY ANY OF THIS MATTERS: actual analysis on long format ----

# sort_values() reorders rows by a column's values.
# ascending=False means largest first (descending order).
# WHY THIS MATTERS: raw groupby results come back in index order,
# not sorted by value. sort_values() makes the ranking immediately readable.
subject_avg = long_format.groupby("subject")["score"].mean().sort_values(ascending=False)
print(f"Average score per subject (best to worst):\n{subject_avg}\n")

# idxmax() returns the INDEX LABEL of the maximum value, not the value itself.
# so groupby("subject")["score"].idxmax() gives us the ROW NUMBERS
# of the highest scorer in each subject group.
# we then pass those row numbers into .loc[] to pull the full rows.
# WHY THIS MATTERS: finding "who" scored highest, not just "what" the
# highest score was, requires idxmax() to get the position, then loc[]
# to retrieve the actual row data at that position.
top_per_subject = long_format.loc[
    long_format.groupby("subject")["score"].idxmax(),
    ["subject", "name", "score"]
]
print(f"Top scorer per subject:\n{top_per_subject}\n")

# idxmin() is the same as idxmax() but for the MINIMUM value.
# here we use it on std() results, so it returns the name of the
# student whose score standard deviation is lowest across subjects,
# meaning their scores are most tightly clustered around their own mean.
# std() = standard deviation, same concept from Day 21, how spread
# out a set of values is. Low std = consistent. High std = uneven.
consistency = long_format.groupby("name")["score"].std().sort_values()
print(f"Most consistent students (lowest std across subjects):\n{consistency}\n")
print(f"Most consistent student : {consistency.idxmin()} (std={consistency.min():.2f})\n")

city_overall = long_format.groupby("city")["score"].mean().sort_values(ascending=False)
print(f"Best performing city overall:\n{city_overall}\n")

print("=" * 45)
print("  ANALYSIS SUMMARY")
print("=" * 45)
print(f"  Best subject overall : {subject_avg.idxmax()} ({subject_avg.max():.1f} avg)")
print(f"  Hardest subject      : {subject_avg.idxmin()} ({subject_avg.min():.1f} avg)")
print(f"  Most consistent      : {consistency.idxmin()} (std={consistency.min():.2f})")
print(f"  Top city             : {city_overall.idxmax()} ({city_overall.max():.1f} avg)")