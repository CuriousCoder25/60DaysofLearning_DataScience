import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.ion()

students = pd.DataFrame({
    "name":       ["Gaurav", "Alice", "Pino", "Diana", "Evren",
                   "Frank", "Grace", "Henry", "Iris", "Jack"],
    "study_hours":[4, 6, 3, 7, 5, 2, 8, 4, 6, 3],
    "sleep_hours":[7, 6, 5, 8, 7, 4, 8, 6, 7, 5],
    "score":      [88, 92, 75, 95, 81, 65, 97, 80, 90, 70],
    "city":       ["Dhangadhi", "Pokhara", "Kathmandu", "Butwal", "Pokhara",
                   "Butwal", "Kathmandu", "Pokhara", "Butwal", "Kathmandu"],
    "grade":      ["B", "A", "C", "A", "B", "F", "A", "B", "A", "C"]
})

# sns.set_theme() applies a global aesthetic to ALL plots below it.
# style= controls the background grid ("darkgrid", "whitegrid", "dark", "white", "ticks")
# palette= sets the default color scheme for categorical variables.
# WHY THIS MATTERS: one line makes every chart look polished without
# manually setting colors, grids, and fonts on each individual plot.
sns.set_theme(style="whitegrid", palette="muted")

# PART 1: sns.histplot : better histogram than plt.hist()
# kde=True overlays a Kernel Density Estimate curve on top of the bars.
# KDE is a smoothed continuous version of the histogram, showing the
# overall distribution shape without being tied to bin boundaries.
# hue= splits the distribution by a categorical variable automatically.
plt.figure(figsize=(8, 5), num="Histogram with KDE")

sns.histplot(students["score"],
    bins=6,
    kde=True,          # adds the smooth curve on top
    color="steelblue"
)

plt.title("Score Distribution with KDE", fontsize=14, fontweight="bold")
plt.xlabel("Score")
plt.ylabel("Count")
plt.tight_layout()
plt.show(block=False)

# PART 2: sns.scatterplot : scatter with built-in hue and size encoding
# hue= automatically assigns colors per category and builds the legend.
# size= scales dot size by a numeric column automatically.
# This replaces the manual groupby loop from Day 42 Part 3 and 4
# with a single function call : same result, far less code.
plt.figure(figsize=(9, 5), num="Scatter Plot - Hue and Size")

sns.scatterplot(
    data=students,
    x="study_hours",
    y="score",
    hue="city",        # color by city
    size="sleep_hours", # dot size by sleep hours
    sizes=(50, 200),   # min and max dot size range
    palette={
        "Dhangadhi": "goldenrod",
        "Kathmandu": "steelblue",
        "Pokhara":   "coral",
        "Butwal":    "mediumseagreen"
    },
    alpha=0.8
)

plt.title("Study Hours vs Score (Seaborn)", fontsize=14, fontweight="bold")
plt.xlabel("Study Hours per Day")
plt.ylabel("Score")
plt.tight_layout()
plt.show(block=False)

# PART 3: sns.boxplot : same concept as Day 41 but cleaner syntax
# orient="v" means vertical boxes (default), one per grade category.
# hue= splits boxes by an additional variable if needed.
# order= controls the left-to-right order of categories on x axis.
plt.figure(figsize=(8, 5), num="Box Plot - Score Per Grade")

sns.boxplot(
    data=students,
    x="grade",
    y="score",
    palette="muted",
    order=["A", "B", "C", "F"]   # explicit order so F doesn't appear first
)

plt.title("Score Distribution per Grade", fontsize=14, fontweight="bold")
plt.xlabel("Grade")
plt.ylabel("Score")
plt.tight_layout()
plt.show(block=False)

# PART 4: sns.violinplot : upgrade from box plot
# violin plot = box plot + KDE rotated on its side.
# the width of the violin at each point shows how many values
# fall in that range, thicker = more students scored there.
# WHY THIS MATTERS: box plots hide whether data is unimodal
# (one peak) or bimodal (two peaks). violin plots reveal that shape.
plt.figure(figsize=(8, 5), num="Violin Plot- Score Per Grade")

sns.violinplot(
    data=students,
    x="grade",
    y="score",
    palette="muted",
    order=["A", "B", "C", "F"],
    inner="quartile"   # draws quartile lines inside the violin
)

plt.title("Score Distribution per Grade (Violin)", fontsize=14, fontweight="bold")
plt.xlabel("Grade")
plt.ylabel("Score")
plt.tight_layout()
plt.show(block=False)

# PART 5: sns.pairplot : automatic scatter matrix
# pairplot creates a grid of scatter plots for EVERY pair of
# numeric columns in the dataset at once, with histograms on
# the diagonal showing each variable's own distribution.
# hue= colors every plot by a categorical variable simultaneously.
# WHY THIS MATTERS: on a new dataset this is the single fastest
# way to visually scan ALL pairwise relationships at once before
# deciding which ones are worth investigating further.
pair = sns.pairplot(
    students[["study_hours", "sleep_hours", "score", "grade"]],
    hue="grade",
    palette="muted",
    diag_kind="kde"    # kde on diagonal instead of histogram
)

pair.fig.suptitle("Pairplot of Student Features", y=1.02,
    fontsize=14, fontweight="bold")
pair.fig.canvas.manager.set_window_title("Pair Plot - All Features")
plt.show(block=False)

plt.ioff()
plt.show()