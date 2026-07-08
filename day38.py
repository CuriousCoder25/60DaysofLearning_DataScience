import pandas as pd
import numpy as np

# RAW DATASET: this dataset intentionally contains common problems
# found in real-world data:
# - duplicate rows
# - missing values
# - inconsistent capitalization
# - extra spaces
#
# Our goal today is to perform a complete EDA pipeline:
# clean -> analyze -> summarize -> export

students = pd.DataFrame({
    "student_id":[101,102,103,104,101,105,106,107],
    "name":["Gaurav"," Alice ","pino",None,"Gaurav","Eva","alice","PINO"],
    "city":["Kathmandu","Pokhara","pokhara","Kathmandu",
            "Kathmandu","Biratnagar","Pokhara","Biratnagar"],
    "course":["Python","Python","Data Science","Python",
              "Python","Data Science","Python","Data Science"],
    "score":[88,np.nan,75,91,88,84,np.nan,79]
})

print(f"Raw dataset:\n{students}\n")

# info() gives an overview of the dataset:
# - number of rows
# - missing values
# - data types
#
# This is usually the first thing we inspect before cleaning.

print(students.info())

# describe() summarizes every numeric column.
# It helps us quickly understand the distribution of values.

print(f"\nSummary statistics:\n{students.describe()}\n")

# isna().sum() counts missing values in each column.

print(f"Missing values:\n{students.isna().sum()}\n")

# drop_duplicates() removes identical rows.
# Duplicate records commonly appear when data is exported
# multiple times.

students = students.drop_duplicates()

print(f"After removing duplicates:\n{students}\n")

# fillna() replaces missing values.
# Missing names become "Unknown".
# Missing scores become the average score.

students["name"] = students["name"].fillna("Unknown")
students["score"] = students["score"].fillna(
    students["score"].mean()
)

print(f"After filling missing values:\n{students}\n")

# Real datasets often contain inconsistent text formatting.
#
# " Alice "
# "alice"
# "ALICE"
#
# should all become "Alice".

students["name"] = students["name"].str.strip().str.title()
students["city"] = students["city"].str.strip().str.title()
students["course"] = students["course"].str.strip().str.title()

print(f"After standardizing text:\n{students}\n")

# Feature engineering means creating a new useful column.
# Here we convert numeric scores into Pass or Fail.

students["result"] = students["score"].apply(
    lambda score: "Pass" if score >= 40 else "Fail"
)

print(f"Dataset after feature engineering:\n{students}\n")

# groupby() splits the data into groups,
# performs calculations on each group,
# and combines the results.

city_summary = students.groupby("city").agg({
    "student_id":"count",
    "score":["mean","max","min"]
})

print(f"Summary by city:\n{city_summary}\n")

# Average score for each course.

course_summary = students.groupby("course")["score"].mean()

print(f"Average score by course:\n{course_summary}\n")

# Count how many students passed and failed.

result_summary = students.groupby("result")["student_id"].count()

print(f"Pass/Fail count:\n{result_summary}\n")

# Once the analysis is complete,
# we export the summary so it can be used elsewhere.

city_summary.to_csv("city_summary_report.csv")

print("Summary report exported successfully!")
print("Saved as: city_summary_report.csv")