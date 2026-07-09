import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# MATPLOTLIB'S CORE CONCEPT: every plot has two layers.
# Figure = the entire canvas/window, like a blank sheet of paper.
# Axes = the actual plot area inside the figure, where data is drawn.
# plt.subplots() creates both at once and returns them separately.
# WHY THIS MATTERS: understanding figure vs axes is what lets us
# put multiple plots side by side, which we'll do in the milestone.
fig, ax = plt.subplots()

# simple line plot on the axes object directly
x = [1, 2, 3, 4, 5]
y = [10, 25, 18, 35, 28]

ax.plot(x, y)
ax.set_title("Basic Line Plot")
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
plt.show()

# PART 2: customizing the plot
# color, linewidth, marker, linestyle are the four most common
# visual tweaks we'll use constantly in every plot going forward
fig, ax = plt.subplots(figsize=(8, 4))   # figsize controls width x height in inches

ax.plot(x, y,
    color="steelblue",
    linewidth=2,
    marker="o",          # circle marker at each data point
    linestyle="--",      # dashed line
    label="Monthly scores"
)

ax.set_title("Customized Line Plot", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Score")
ax.legend()             # shows the label we set above
ax.grid(True, alpha=0.3)  # light grid helps readability
plt.tight_layout()      # prevents labels from getting clipped at edges
plt.show()

# PART 3: multiple subplots on one figure
# subplots(1, 2) = 1 row, 2 columns of plots side by side.
# ax is now an ARRAY of axes, one per subplot.
# WHY THIS MATTERS: the milestone dashboard (Day 46) is just
# this idea scaled up to a 2x2 or larger grid of subplots.
students = pd.DataFrame({
    "name":  ["Gaurav", "Alice", "Pino", "Diana", "Evren"],
    "score": [88, 92, 75, 95, 81],
    "age":   [21, 22, 20, 23, 21]
})

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# left subplot
axes[0].bar(students["name"], students["score"], color="steelblue")
axes[0].set_title("Score per Student")
axes[0].set_xlabel("Student")
axes[0].set_ylabel("Score")

# right subplot
axes[1].plot(students["age"], students["score"],
    marker="o", color="coral", linewidth=2)
axes[1].set_title("Age vs Score")
axes[1].set_xlabel("Age")
axes[1].set_ylabel("Score")

plt.suptitle("Student Overview", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.show()

# PART 4: saving a plot to file instead of just showing it
# savefig() exports to PNG, PDF, SVG — just change the extension.
# dpi=150 controls resolution, higher = sharper but larger file.
# WHY THIS MATTERS: the milestone dashboard gets EXPORTED as a file,
# not just shown in a window, so savefig() is essential to know.
fig.savefig("student_overview.png", dpi=150, bbox_inches="tight")
print("Plot saved to student_overview.png")