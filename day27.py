import pandas as pd

# pd.read_csv() is the single most-used Pandas function in real
# data science , almost every project starts by loading a CSV.
# This connects to Day 13's file I/O , same idea (open and read a file),
# but Pandas parses it directly into a structured DataFrame for you,
# no manual csv.reader loop needed.
students = pd.DataFrame({
    "name": ["Gaurav", "Alice", "Bob", "Diana", "Eve"],
    "age": [21, 22, 20, 23, 21],
    "city": ["Kathmandu", "Pokhara", "Dhangadhi", "Butwal", "Biratnagar"],
    "score": [88, 92, 75, 95, 81]
})

# .to_csv() writes a DataFrame to disk , index=False skips writing
# the row numbers as a column, since you usually don't want that
# duplicated when you reopen the file later.
students.to_csv("students.csv", index=False)
print("students.csv written\n")

# Now read it back , this is the realistic workflow: someone else
# (or your past self) already created the CSV, and you're loading it fresh
loaded = pd.read_csv("students.csv")
print(f"Loaded from CSV:\n{loaded}\n")

# WHY THIS MATTERS: read_csv automatically detects column types ,
# 'age' and 'score' become numbers, 'name' and 'city' stay text.
# You didn't have to cast anything manually, unlike Day 14's
# CSV parsing where you had to convert strings to int yourself.
print(f"Dtypes after reading:\n{loaded.dtypes}\n")

# Common read_csv parameters worth knowing:
# - usecols: only load specific columns (saves memory on big files)
# - nrows: only load the first N rows (great for peeking at huge files)
partial = pd.read_csv("students.csv", usecols=["name", "score"], nrows=3)
print(f"Partial load (2 cols, 3 rows):\n{partial}\n")

# Excel files work almost identically , same function family,
# just swap read_csv for read_excel. Requires: pip install openpyxl
students.to_excel("students.xlsx", index=False, engine="openpyxl")
excel_loaded = pd.read_excel("students.xlsx")
print(f"Loaded from Excel:\n{excel_loaded}\n")

# REAL PATTERN: exporting a filtered/processed subset, not just the raw data , this is what is done constantly in real projects
top_scorers = loaded[loaded["score"] >= 85]
top_scorers.to_csv("top_scorers.csv", index=False)
print(f"Top scorers exported:\n{top_scorers}")