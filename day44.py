import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.ion()
sns.set_theme(style="whitegrid", palette="muted")

students = pd.DataFrame({
    "name":        ["Gaurav", "Alice", "Pino", "Diana", "Evren",
                    "Frank", "Grace", "Henry", "Iris", "Jack"],
    "study_hours": [4, 6, 3, 7, 5, 2, 8, 4, 6, 3],
    "sleep_hours": [7, 6, 5, 8, 7, 4, 8, 6, 7, 5],
    "score":       [88, 92, 75, 95, 81, 65, 97, 80, 90, 70],
    "attendance":  [85, 90, 70, 95, 88, 60, 98, 82, 91, 72],
    "assignments": [9, 10, 7, 10, 8, 5, 10, 8, 9, 6]
})

# .corr() computes the Pearson correlation coefficient between
# every pair of numeric columns and returns a correlation MATRIX.
# values range from -1 to 1:
# 1  = perfect positive correlation (both go up together)
# -1 = perfect negative correlation (one goes up, other goes down)
# 0  = no linear relationship at all
# WHY THIS MATTERS: before building any ML model, we check the
# correlation matrix to understand which features actually relate
# to the target variable and which ones relate to each other
# (multicollinearity — a problem we'll deal with in Phase 5).
corr_matrix = students.drop(columns="name").corr()
print(f"Correlation matrix:\n{corr_matrix}\n")

# PART 1: basic heatmap
# sns.heatmap() visualizes the correlation matrix as a color grid.
# annot=True prints the actual correlation value inside each cell.
# fmt=".2f" formats those numbers to 2 decimal places.
# cmap= sets the color scheme. "coolwarm" = blue (negative) to red (positive).
# vmin/vmax= pins the color scale so 1 is always darkest red and
# -1 is always darkest blue, regardless of actual data range.
plt.figure(figsize=(8, 6), num="Correlation Heatmap")

sns.heatmap(corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1, vmax=1,
    linewidths=0.5,      # thin lines between cells for readability
    square=True          # forces each cell to be square shaped
)

plt.title("Feature Correlation Matrix", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show(block=False)

# PART 2: masking the upper triangle
# the correlation matrix is SYMMETRIC — the value at [row, col]
# is always identical to [col, row]. showing both sides is redundant.
# np.triu() returns the upper triangle of a matrix as True/False.
# passing that mask to heatmap hides the upper triangle entirely,
# making the chart cleaner and easier to read.
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

plt.figure(figsize=(8, 6), num="Correlation Heatmap - Lower Triangle")

sns.heatmap(corr_matrix,
    mask=mask,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1, vmax=1,
    linewidths=0.5,
    square=True
)

plt.title("Correlation Matrix (Lower Triangle Only)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show(block=False)

# PART 3: extracting the most important correlations programmatically
# reading a heatmap visually is fine for small matrices, but for
# datasets with 20+ features we need to extract top correlations in code.
# .unstack() converts the matrix into a Series of (col1, col2) pairs.
# we then filter out self-correlations (where col1 == col2, always 1.0)
# and sort by absolute value to find the strongest relationships.
corr_pairs = corr_matrix.unstack()
corr_pairs = corr_pairs[corr_pairs.index.get_level_values(0) !=
                         corr_pairs.index.get_level_values(1)]
corr_pairs = corr_pairs.abs().sort_values(ascending=False)

print("Top feature correlations (by absolute value):")
print(corr_pairs.drop_duplicates().head(10))

# PART 4: correlation with the TARGET variable only
# in ML we usually care most about "which features correlate
# with the thing we're trying to predict?" not every pair.
# here: score is our target, so we isolate just that column.
target_corr = corr_matrix["score"].drop("score").sort_values(ascending=False)
print(f"\nCorrelation with score (target variable):\n{target_corr}\n")

plt.figure(figsize=(6, 4), num="Feature Correlation with Score")

sns.barplot(x=target_corr.values, y=target_corr.index,
    palette="coolwarm_r",
    orient="h"
)

plt.axvline(x=0, color="black", linewidth=0.8)
plt.title("Feature Correlation with Score", fontsize=14, fontweight="bold")
plt.xlabel("Correlation Coefficient")
plt.tight_layout()
plt.show(block=False)

plt.ioff()
plt.show()