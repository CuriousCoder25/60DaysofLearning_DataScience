import pandas as pd

# A Pandas Series is just a labeled 1D array, think of it as one column of a spreadsheet, with an index attached to each value.
# This connects directly back to NumPy arrays (i did this on Day 16), Series are BUILT on top of NumPy arrays, just with labels added.
ages = pd.Series([21, 22, 20, 23, 21], name="age")
print(f"Series:\n{ages}\n")
print(f"Values (still a NumPy array underneath): {ages.values}")
print(f"Index : {ages.index}\n")

# A DataFrame is the real workhorse - think of it as a full spreadsheet: multiple columns, each one technically a Series,
# all sharing the same row index. THIS is what you'll use 95% of the time in real data science work, not raw NumPy arrays.
students = pd.DataFrame({
    "name": ["Gaurav", "Bikesh", "Khasi", "Durge", "Aaley"],
    "age": [21, 22, 20, 23, 21],
    "city": ["Dhangadhi", "Pokhara", "Dhangadhi", "Butwal", "Biratnagar"],
    "score": [88, 92, 75, 95, 81]
})

print(f"Full DataFrame:\n{students}\n")

# THE WHY: a NumPy array can't mix data types cleanly - names (text) and scores (numbers) together would be messy.
# DataFrames handle mixed types per column naturally, which is exactly what real-world data looks like (names + numbers + dates).
print(f"Column types:\n{students.dtypes}\n")

# Quick structural overview - your first move on ANY new dataset
print(f"Shape (rows, cols): {students.shape}")
print(f"Column names      : {list(students.columns)}")

# .head() shows the first few rows - essential first check on large datasets where printing everything would flood your screen
print(f"\nFirst 3 rows:\n{students.head(3)}\n")

# .describe() gives instant summary statistics on numeric columns - this is Day 21's mean/std aggregation, but Pandas does it for
# EVERY numeric column automatically, no manual axis= needed
print(f"Quick stats:\n{students.describe()}\n")

# Selecting a single column returns a Series - proving DataFrames really are just a collection of Series glued together by index
print(f"Just the 'score' column (a Series):\n{students['score']}")