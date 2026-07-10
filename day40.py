import pandas as pd
import matplotlib.pyplot as plt

# Turn on interactive mode so each figure opens without
# blocking the execution of the rest of the script.
plt.ion()

# LINE CHARTS VS HISTOGRAMS
#
# Both visualize numerical data, but they answer different questions.
#
# Line Chart:
#   - shows how values change over time or another ordered sequence.
#   - useful for identifying trends.
#
# Histogram:
#   - shows how values are distributed.
#   - useful for understanding frequency, spread, and skewness.

students = pd.DataFrame({
    "week": [1, 2, 3, 4, 5, 6, 7, 8],
    "average_score": [68, 72, 70, 76, 81, 84, 87, 91]
})

exam_scores = pd.DataFrame({
    "student": [
        "Alice", "Bob", "Charlie", "David", "Eva",
        "Frank", "Grace", "Helen", "Ian", "Jack",
        "Kevin", "Luna", "Mike", "Nina", "Oscar"
    ],
    "score": [
        72, 84, 91, 65, 77,
        88, 93, 70, 81, 76,
        95, 69, 87, 79, 90
    ]
})

print(f"Weekly average scores:\n{students}\n")
print(f"Exam scores:\n{exam_scores}\n")

# A LINE CHART connects data points in order.
# WHY THIS MATTERS:
# It is best used when the x-axis represents time or another
# ordered sequence, making it easy to identify trends such as
# growth, decline, or seasonal patterns.

plt.figure(figsize=(8, 4))

plt.plot(
    students["week"],
    students["average_score"],
    marker="o",
    linewidth=2,
    color="steelblue",
    label="Average Score"
)

plt.title("Average Student Score Over 8 Weeks")
plt.xlabel("Week")
plt.ylabel("Average Score")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

# block=False allows the program to continue creating
# the remaining figures instead of waiting for this one
# to be closed.
plt.show(block=False)

# A HISTOGRAM groups numerical values into intervals called bins.
#
# WHY THIS MATTERS:
# Instead of showing how values change over time,
# it shows how frequently different ranges of values occur.
# This helps us understand the distribution of a dataset.

plt.figure(figsize=(8, 4))

plt.hist(
    exam_scores["score"],
    bins=5,
    edgecolor="black",
    color="coral"
)

plt.title("Distribution of Student Exam Scores")
plt.xlabel("Score")
plt.ylabel("Frequency")

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.show(block=False)

# bins controls how many intervals the data is divided into.
#
# More bins = more detail.
# Fewer bins = smoother distribution.
#
# Choosing an appropriate number of bins makes patterns
# easier to interpret.

plt.figure(figsize=(8, 4))

plt.hist(
    exam_scores["score"],
    bins=10,
    edgecolor="black",
    color="mediumseagreen"
)

plt.title("Distribution of Student Scores (10 Bins)")
plt.xlabel("Score")
plt.ylabel("Frequency")

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.show(block=False)

# Basic descriptive statistics summarize the dataset numerically.
# These values complement visualizations by providing exact
# measurements for the center and spread of the data.

print(f"Average Score: {exam_scores['score'].mean():.2f}")
print(f"Median Score: {exam_scores['score'].median():.2f}")
print(f"Highest Score: {exam_scores['score'].max()}")
print(f"Lowest Score: {exam_scores['score'].min()}")

# INTERPRETATION
#
# Line Chart:
# "How did average scores change from week to week?"
#
# Histogram:
# "Which score ranges occurred most frequently?"
#
# Although both plots visualize numerical data,
# they answer completely different analytical questions.

# Turn interactive mode off and keep all figure windows open
# until the user closes them.
plt.ioff()
plt.show()