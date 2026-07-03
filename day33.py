import pandas as pd
import numpy as np

students = pd.DataFrame({
    "name":   ["Gaurav", "Alice", "Bob", "Diana", "Eve", "Frank", "Grace", "Henry"],
    "city":   ["Kathmandu", "Pokhara", "Kathmandu", "Butwal", "Pokhara", "Butwal", "Kathmandu", "Pokhara"],
    "grade":  ["A", "A", "B", "A", "C", "B", "A", "B"],
    "score":  [88, 92, 75, 95, 81, 70, 90, 78],
    "age":    [21, 22, 20, 23, 21, 24, 22, 21]
})
print(f"DataFrame:\n{students}\n")

# THE CORE CONCEPT: GroupBy splits the DataFrame into groups
# based on a column, applies a function to each group separately,
# then combines the results back into one clean summary table.
# WHY THIS MATTERS: this is the single most common pattern in
# real data analysis. "Average sales per region", "total orders
# per customer", "max score per grade" all use this exact pattern.

# PART 1: basic groupby on one column
# split students into groups by city, then compute mean per group
city_avg = students.groupby("city")["score"].mean()
print(f"Average score per city:\n{city_avg}\n")

# PART 2: multiple aggregations on one column
# instead of running .mean() then .sum() separately, .agg() does
# all of them in one pass and gives us a clean summary table
city_stats = students.groupby("city")["score"].agg(["mean", "sum", "min", "max", "count"])
print(f"Score stats per city:\n{city_stats}\n")

# PART 3: groupby on multiple columns at once
# split by both city AND grade, compute mean score for each combo
city_grade_avg = students.groupby(["city", "grade"])["score"].mean()
print(f"Average score per city and grade:\n{city_grade_avg}\n")

# PART 4: custom aggregation with named outputs
# .agg() with a dict lets us name our output columns cleanly,
# much more readable than renaming columns after the fact
city_summary = students.groupby("city")["score"].agg(
    avg_score="mean",
    top_score="max",
    student_count="count"
)
print(f"Named aggregations per city:\n{city_summary}\n")

# PART 5: groupby with transform
# .transform() is different from .agg() in a key way:
# .agg() collapses each group into ONE summary row
# .transform() keeps the ORIGINAL shape, broadcasting the
# group result back to every row that belongs to that group.
# WHY THIS MATTERS: we can add a "city average" column to every
# student row, making it easy to compare individual vs group performance
students["city_avg_score"] = students.groupby("city")["score"].transform("mean")
students["vs_city_avg"] = students["score"] - students["city_avg_score"]
print(f"Students vs their city average:\n{students[['name', 'city', 'score', 'city_avg_score', 'vs_city_avg']]}\n")

# PART 6: groupby with filter
# keep only groups where the average score is above 82
high_performing_cities = students.groupby("city").filter(lambda g: g["score"].mean() > 82)
print(f"Students from high-performing cities (avg > 82):\n{high_performing_cities}")