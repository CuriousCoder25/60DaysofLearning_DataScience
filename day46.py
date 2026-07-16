import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")

# FULL DATASET: combining everything we've built across Phase 3 and 4
students = pd.DataFrame({
    "name":        ["Gaurav", "Alice", "Pino", "Diana", "Evren",
                    "Frank", "Grace", "Henry", "Iris", "Jack"],
    "study_hours": [4, 6, 3, 7, 5, 2, 8, 4, 6, 3],
    "sleep_hours": [7, 6, 5, 8, 7, 4, 8, 6, 7, 5],
    "score":       [88, 92, 75, 95, 81, 65, 97, 80, 90, 70],
    "attendance":  [85, 90, 70, 95, 88, 60, 98, 82, 91, 72],
    "assignments": [9, 10, 7, 10, 8, 5, 10, 8, 9, 6],
    "city":        ["Dhangadhi", "Pokhara", "Kathmandu", "Butwal", "Pokhara",
                    "Butwal", "Kathmandu", "Pokhara", "Butwal", "Kathmandu"],
    "grade":       ["B", "A", "C", "A", "B", "F", "A", "B", "A", "C"]
})

weekly = pd.DataFrame({
    "week":          [1, 2, 3, 4, 5, 6, 7, 8],
    "average_score": [68, 72, 70, 76, 81, 84, 87, 91]
})

city_colors = {
    "Dhangadhi": "goldenrod",
    "Kathmandu": "steelblue",
    "Pokhara":   "coral",
    "Butwal":    "mediumseagreen"
}

# gridspec gives us fine-grained control over subplot layout.
# unlike plt.subplots() which creates a uniform grid, GridSpec
# lets panels span multiple rows or columns, useful for dashboards
# where some charts deserve more real estate than others.
# WHY THIS MATTERS: a real dashboard isn't a uniform grid,
# the most important chart usually gets more space.
fig = plt.figure(figsize=(18, 12))
fig.suptitle("Student Performance Dashboard", fontsize=20,
    fontweight="bold", y=0.98)

gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

# ---- PANEL 1: KPI summary text (top left, spans 1 col) ----
# text panels are a standard dashboard element, showing key numbers
# at a glance before the viewer digs into the charts below.
ax_kpi = fig.add_subplot(gs[0, 0])
ax_kpi.axis("off")   # turn off axes lines and ticks, text only

kpis = [
    ("Total Students",  len(students)),
    ("Avg Score",       f"{students['score'].mean():.1f}"),
    ("Top Score",       students['score'].max()),
    ("Avg Attendance",  f"{students['attendance'].mean():.1f}%"),
    ("Avg Study Hours", f"{students['study_hours'].mean():.1f} hrs"),
    ("Pass Rate",       f"{(students['score'] >= 75).mean()*100:.0f}%"),
]

ax_kpi.text(0.05, 0.95, "Key Metrics", fontsize=13,
    fontweight="bold", transform=ax_kpi.transAxes, va="top")

for i, (label, value) in enumerate(kpis):
    ax_kpi.text(0.05, 0.80 - i * 0.13, f"{label}:", fontsize=10,
        color="gray", transform=ax_kpi.transAxes, va="top")
    ax_kpi.text(0.60, 0.80 - i * 0.13, str(value), fontsize=10,
        fontweight="bold", transform=ax_kpi.transAxes, va="top")

# ---- PANEL 2: weekly trend line (top middle, spans 2 cols) ----
ax_trend = fig.add_subplot(gs[0, 1:])   # spans columns 1 and 2

ax_trend.plot(weekly["week"], weekly["average_score"],
    marker="o", linewidth=2.5, color="steelblue", label="Avg Score")
ax_trend.fill_between(weekly["week"], weekly["average_score"],
    alpha=0.15, color="steelblue")   # shaded area under line, adds visual depth
ax_trend.set_title("Weekly Score Trend", fontweight="bold")
ax_trend.set_xlabel("Week")
ax_trend.set_ylabel("Average Score")
ax_trend.set_ylim(60, 100)
ax_trend.grid(True, alpha=0.3)

# ---- PANEL 3: bar chart — score per student (middle left, spans 2 cols) ----
ax_bar = fig.add_subplot(gs[1, :2])   # spans columns 0 and 1

colors = [city_colors[c] for c in students["city"]]
ax_bar.bar(students["name"], students["score"],
    color=colors, edgecolor="white", width=0.6)
ax_bar.axhline(y=students["score"].mean(),
    color="red", linestyle="--", linewidth=1.5,
    label=f"Mean ({students['score'].mean():.1f})")
ax_bar.set_title("Score per Student (color = city)", fontweight="bold")
ax_bar.set_xlabel("Student")
ax_bar.set_ylabel("Score")
ax_bar.legend(fontsize=9)
ax_bar.grid(axis="y", alpha=0.3)
ax_bar.tick_params(axis="x", rotation=30)

# ---- PANEL 4: box plot — distribution per grade (middle right) ----
ax_box = fig.add_subplot(gs[1, 2])

sns.boxplot(data=students, x="grade", y="score",
    palette="muted", order=["A", "B", "C", "F"], ax=ax_box)
ax_box.set_title("Score Distribution by Grade", fontweight="bold")
ax_box.set_xlabel("Grade")
ax_box.set_ylabel("Score")

# ---- PANEL 5: scatter plot — study hours vs score (bottom left) ----
ax_scatter = fig.add_subplot(gs[2, 0])

for city, group in students.groupby("city"):
    ax_scatter.scatter(group["study_hours"], group["score"],
        color=city_colors[city], s=80, alpha=0.8, label=city)

coeffs = np.polyfit(students["study_hours"], students["score"], 1)
x_line = np.linspace(students["study_hours"].min(),
                     students["study_hours"].max(), 100)
ax_scatter.plot(x_line, np.poly1d(coeffs)(x_line),
    color="red", linestyle="--", linewidth=1.5)
ax_scatter.set_title("Study Hours vs Score", fontweight="bold")
ax_scatter.set_xlabel("Study Hours")
ax_scatter.set_ylabel("Score")
ax_scatter.legend(fontsize=7, title="City", title_fontsize=8)

# ---- PANEL 6: heatmap — correlation matrix (bottom middle) ----
ax_heat = fig.add_subplot(gs[2, 1])

corr = students[["score", "study_hours", "sleep_hours",
                  "attendance", "assignments"]].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
    cmap="coolwarm", vmin=-1, vmax=1,
    linewidths=0.5, square=True, ax=ax_heat,
    annot_kws={"size": 8})
ax_heat.set_title("Correlation Matrix", fontweight="bold")

# ---- PANEL 7: horizontal bar — city average score (bottom right) ----
ax_city = fig.add_subplot(gs[2, 2])

city_avg = students.groupby("city")["score"].mean().sort_values()
ax_city.barh(city_avg.index, city_avg.values,
    color=[city_colors[c] for c in city_avg.index],
    edgecolor="white")
ax_city.set_title("Avg Score by City", fontweight="bold")
ax_city.set_xlabel("Average Score")
ax_city.grid(axis="x", alpha=0.3)
ax_city.set_xlim(70, 100)

# export the full dashboard as a high-resolution PNG
plt.savefig("student_kpi_dashboard.png", dpi=150,
    bbox_inches="tight", facecolor="white")
print("Dashboard saved to student_kpi_dashboard.png")
plt.show()