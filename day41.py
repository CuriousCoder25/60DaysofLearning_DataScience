import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

students = pd.DataFrame({
    "name":    ["Gaurav", "Alice", "Pino", "Diana", "Evren", "Frank", "Grace", "Henry"],
    "city":    ["Kathmandu", "Pokhara", "Kathmandu", "Butwal", "Pokhara", "Butwal", "Kathmandu", "Pokhara"],
    "math":    [88, 92, 75, 95, 81, 70, 90, 78],
    "science": [90, 85, 78, 88, 76, 65, 91, 82],
    "english": [78, 95, 80, 91, 83, 72, 88, 74]
})

# PART 1: basic bar chart — categorical comparison
# bar charts answer "how does each category compare on one metric?"
# x axis = categories (names), y axis = numeric value (score)
fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(students["name"], students["math"],
    color="steelblue",
    edgecolor="white",
    width=0.6
)
ax.set_title("Math Scores per Student", fontsize=14, fontweight="bold")
ax.set_xlabel("Student")
ax.set_ylabel("Score")
ax.axhline(y=students["math"].mean(), color="red",
    linestyle="--", linewidth=1.5, label=f"Mean ({students['math'].mean():.1f})")
ax.legend()
ax.grid(axis="y", alpha=0.3)   # horizontal grid lines only, cleaner for bar charts
plt.tight_layout()
plt.show()

# PART 2: grouped bar chart — comparing multiple categories at once
# shows math vs science vs english side by side per student
# WHY THIS MATTERS: when we have more than one metric per category,
# grouped bars let us compare across both dimensions simultaneously

x = np.arange(len(students["name"]))  # positions for each student on x axis
width = 0.25                           # width of each individual bar

fig, ax = plt.subplots(figsize=(12, 5))

# offset each subject's bars by width so they sit side by side
ax.bar(x - width, students["math"],    width, label="Math",    color="steelblue")
ax.bar(x,         students["science"], width, label="Science", color="coral")
ax.bar(x + width, students["english"], width, label="English", color="mediumseagreen")

ax.set_title("Scores per Subject per Student", fontsize=14, fontweight="bold")
ax.set_xlabel("Student")
ax.set_ylabel("Score")
ax.set_xticks(x)
ax.set_xticklabels(students["name"])
ax.legend()
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

# PART 3: box plot — distribution and outlier detection
# a box plot shows 5 things at once for each group:
# minimum, Q1 (25th percentile), median, Q3 (75th percentile), maximum
# dots OUTSIDE the whiskers = outliers, values unusually far from the rest
# WHY THIS MATTERS: bar charts only show averages, which hide spread
# and outliers. Box plots show the FULL distribution shape at a glance.
scores_by_subject = [students["math"], students["science"], students["english"]]

fig, ax = plt.subplots(figsize=(8, 5))

bp = ax.boxplot(scores_by_subject,
    labels=["Math", "Science", "English"],
    patch_artist=True,          # fills boxes with color
    notch=False
)

# color each box differently for readability
colors = ["steelblue", "coral", "mediumseagreen"]
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_title("Score Distribution per Subject", fontsize=14, fontweight="bold")
ax.set_ylabel("Score")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

# PART 4: side by side — bar chart vs box plot on same figure
# this directly shows WHY box plots add information bar charts hide
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# left: bar chart showing only means
means = [students["math"].mean(), students["science"].mean(), students["english"].mean()]
axes[0].bar(["Math", "Science", "English"], means,
    color=["steelblue", "coral", "mediumseagreen"], edgecolor="white")
axes[0].set_title("Mean Scores Only (Bar Chart)")
axes[0].set_ylabel("Score")
axes[0].set_ylim(60, 100)

# right: box plot showing full distribution
axes[1].boxplot(scores_by_subject,
    labels=["Math", "Science", "English"],
    patch_artist=True)
axes[1].set_title("Full Distribution (Box Plot)")
axes[1].set_ylabel("Score")
axes[1].set_ylim(60, 100)

plt.suptitle("Same Data, Different Story", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("bar_vs_boxplot.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved bar_vs_boxplot.png")