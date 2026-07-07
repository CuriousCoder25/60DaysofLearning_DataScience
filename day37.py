import pandas as pd
import numpy as np

# RAW EVENT LOG: dates are strings here, which is exactly how
# they arrive from CSVs. "2026-04-01" looks like a date to us
# but Pandas treats it as plain text until we explicitly convert it.
# WHY THIS MATTERS: you can't sort, filter by range, or extract
# month/year from a string column, only from a proper datetime column.
logs = pd.DataFrame({
    "student_id": [1, 2, 1, 3, 2, 1, 3, 2, 3],
    "name":       ["Gaurav", "Alice", "Gaurav", "Pino", "Alice", "Gaurav", "Pino", "Alice", "Pino"],
    "event":      ["login", "login", "submit", "login", "submit", "submit", "submit", "login", "login"],
    "date":       ["2026-04-01", "2026-04-01", "2026-04-03", "2026-04-05",
                   "2026-04-07", "2026-04-10", "2026-04-12", "2026-04-15", "2026-04-20"],
    "score":      [None, None, 88, None, 92, 85, 75, None, 80]
})

print(f"Raw log (dates as strings):\n{logs}\n")
print(f"Date column type BEFORE conversion: {logs['date'].dtype}\n")

# pd.to_datetime() converts a string column into proper datetime objects.
# format= is optional but speeds up parsing when we know the format.
# WHY THIS MATTERS: after this one line, Pandas understands this column
# as time, not text, unlocking all the time-based operations below.
logs["date"] = pd.to_datetime(logs["date"], format="%Y-%m-%d")
print(f"Date column type AFTER conversion: {logs['date'].dtype}\n")

# THE .dt ACCESSOR: once a column is datetime type, .dt gives us
# access to all date/time components as new columns we can filter on.
# This is similar to .str accessor from Day 29, but for datetime columns.
logs["year"]    = logs["date"].dt.year
logs["month"]   = logs["date"].dt.month
logs["day"]     = logs["date"].dt.day
logs["weekday"] = logs["date"].dt.day_name()   # Monday, Tuesday, etc.
print(f"After extracting date components:\n{logs}\n")

# SORTING BY DATE: sort_values() on a datetime column sorts
# chronologically, earliest first by default.
logs_sorted = logs.sort_values("date")
print(f"Sorted chronologically:\n{logs_sorted}\n")

# FILTERING BY DATE RANGE: datetime columns support comparison
# operators just like numbers, so filtering a range is intuitive.
# pd.Timestamp() converts a string to a datetime object for comparison.
start = pd.Timestamp("2026-04-05")
end   = pd.Timestamp("2026-04-12")
range_filter = logs[(logs["date"] >= start) & (logs["date"] <= end)]
print(f"Events between April 5 and April 12:\n{range_filter}\n")

# TIME DELTA: subtracting two datetime columns gives a timedelta,
# the difference in time between two events as a duration.
# WHY THIS MATTERS: calculating "days since last login", "time to
# complete a task", or "days between purchase and return" all use this.
logs_sorted["days_since_start"] = (logs_sorted["date"] - logs_sorted["date"].min()).dt.days
print(f"Days since first log entry:\n{logs_sorted[['name', 'date', 'days_since_start']]}\n")

# PRACTICAL ANALYSIS: now that dates are proper datetime objects,
# we can ask time-based questions with simple groupby operations.

# Q1: how many events happened per month?
events_per_month = logs.groupby("month")["event"].count()
print(f"Events per month:\n{events_per_month}\n")

# Q2: what was the average score per student on submit events only?
submit_scores = logs[logs["event"] == "submit"].groupby("name")["score"].mean()
print(f"Average submit score per student:\n{submit_scores}\n")

# Q3: which weekday had the most activity?
weekday_activity = logs.groupby("weekday")["event"].count().sort_values(ascending=False)
print(f"Most active weekdays:\n{weekday_activity}")