import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.ion()

students = pd.DataFrame({
    "name":       ["Gaurav", "Alice", "Pino", "Diana", "Evren",
                   "Frank", "Grace", "Henry", "Iris", "Jack"],
    "study_hours":[4, 6, 3, 7, 5, 2, 8, 4, 6, 3],
    "sleep_hours":[7, 6, 5, 8, 7, 4, 8, 6, 7, 5],
    "score":      [88, 92, 75, 95, 81, 65, 97, 80, 90, 70],
    "city":       ["Dhangadhi", "Pokhara", "Kathmandu", "Butwal", "Pokhara",
                   "Butwal", "Kathmandu", "Pokhara", "Butwal", "Kathmandu"]
})

print(f"Dataset:\n{students}\n")

# PART 1: basic scatter plot
# scatter plots answer "is there a relationship between two variables?"
# each dot = one student, x position = study hours, y position = score.
# if dots trend upward left to right, more study hours = higher score.
plt.figure(figsize=(8, 5))

plt.scatter(students["study_hours"], students["score"],
    color="steelblue",
    s=80,           # s controls dot SIZE
    alpha=0.7       # alpha controls transparency, helps when dots overlap
)

plt.title("Study Hours vs Score", fontsize=14, fontweight="bold")
plt.xlabel("Study Hours per Day")
plt.ylabel("Score")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show(block=False)

# PART 2: adding a trend line
# a trend line (line of best fit) makes the correlation direction
# explicit. np.polyfit fits a line to the data, np.poly1d turns
# those coefficients into a callable function we can evaluate.
# WHY THIS MATTERS: eyeballing a scatter plot is subjective,
# a trend line gives an objective visual summary of the direction.
plt.figure(figsize=(8, 5))

plt.scatter(students["study_hours"], students["score"],
    color="steelblue", s=80, alpha=0.7, label="Students")

# fit a degree-1 polynomial (straight line) to the data
coeffs = np.polyfit(students["study_hours"], students["score"], deg=1)
trend_fn = np.poly1d(coeffs)

# generate x values for the trend line and evaluate the function
x_line = np.linspace(students["study_hours"].min(),
                     students["study_hours"].max(), 100)
plt.plot(x_line, trend_fn(x_line),
    color="red", linewidth=2, linestyle="--", label="Trend line")

plt.title("Study Hours vs Score with Trend Line", fontsize=14, fontweight="bold")
plt.xlabel("Study Hours per Day")
plt.ylabel("Score")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show(block=False)

# PART 3: color encoding a third variable
# scatter plots can show THREE variables at once:
# x axis = study hours, y axis = score, color = city.
# color encoding adds a dimension without adding a new axis.
# WHY THIS MATTERS: this is how we visually detect if group
# membership (city, grade, gender) affects the relationship.
city_colors = {
    "Dhangadhi": "goldenrod",
    "Kathmandu": "steelblue",
    "Pokhara":   "coral",
    "Butwal":    "mediumseagreen"
}

plt.figure(figsize=(9, 5))

for city, group in students.groupby("city"):
    plt.scatter(group["study_hours"], group["score"],
        color=city_colors[city],
        s=80, alpha=0.8,
        label=city
    )

plt.title("Study Hours vs Score by City", fontsize=14, fontweight="bold")
plt.xlabel("Study Hours per Day")
plt.ylabel("Score")
plt.legend(title="City")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show(block=False)

# PART 4: size encoding a fourth variable
# we can encode a FOURTH variable using dot size (s parameter).
# here: x = study hours, y = score, color = city, size = sleep hours.
# more dimensions in one chart = richer story, but don't overdo it,
# more than 3 or 4 encodings makes the chart hard to read.
plt.figure(figsize=(10, 6))

for city, group in students.groupby("city"):
    plt.scatter(
        group["study_hours"],
        group["score"],
        color=city_colors[city],
        s=group["sleep_hours"] * 40,   # scale sleep hours to a visible dot size
        alpha=0.7,
        label=city
    )

# annotate each dot with the student's name
for _, row in students.iterrows():
    plt.annotate(row["name"],
        (row["study_hours"], row["score"]),
        textcoords="offset points",
        xytext=(5, 5),     # shift label slightly so it doesn't overlap the dot
        fontsize=8
    )

plt.title("Study Hours vs Score (size = sleep hours)", fontsize=14, fontweight="bold")
plt.xlabel("Study Hours per Day")
plt.ylabel("Score")
plt.legend(title="City")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("scatter_multivariable.png", dpi=150, bbox_inches="tight")
plt.show(block=False)

print("Saved scatter_multivariable.png")

# PART 5: quick correlation check
# before plotting, it's useful to compute the actual correlation
# coefficient to know HOW strong the relationship is numerically.
# .corr() returns values between -1 and 1:
# 1 = perfect positive correlation, -1 = perfect negative, 0 = no relationship
corr_study = students["study_hours"].corr(students["score"])
corr_sleep = students["sleep_hours"].corr(students["score"])

print(f"\nCorrelation: study hours vs score : {corr_study:.2f}")
print(f"Correlation: sleep hours vs score : {corr_sleep:.2f}")
print(f"\nInterpretation:")
print(f"  study_hours correlation ({corr_study:.2f}) : {'strong' if abs(corr_study) > 0.7 else 'moderate' if abs(corr_study) > 0.4 else 'weak'} positive relationship")
print(f"  sleep_hours correlation ({corr_sleep:.2f}) : {'strong' if abs(corr_sleep) > 0.7 else 'moderate' if abs(corr_sleep) > 0.4 else 'weak'} positive relationship")

plt.ioff()
plt.show()