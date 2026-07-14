import pandas as pd
import numpy as np
import plotly.express as px

# PLOTLY vs MATPLOTLIB/SEABORN:
# Matplotlib and Seaborn produce STATIC images, what we see is fixed.
# Plotly produces INTERACTIVE charts, we can zoom, pan, hover over
# individual data points and see their exact values, toggle legend
# items on and off, and export directly from the browser window.
# WHY THIS MATTERS: static charts are for reports and papers.
# Interactive charts are for dashboards and exploratory analysis
# where we want to dig into specific data points on the fly.

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

# weekly score trend : simulating a time series
weekly = pd.DataFrame({
    "week":          [1, 2, 3, 4, 5, 6, 7, 8],
    "average_score": [68, 72, 70, 76, 81, 84, 87, 91],
    "top_score":     [75, 80, 78, 85, 88, 91, 94, 97],
    "low_score":     [55, 60, 58, 65, 72, 75, 78, 82]
})

# PART 1: px.line : interactive line chart
# hover_data= adds extra columns to the tooltip that appears
# when we hover over a data point. title= sets the chart title.
# markers=True adds dots at each data point like plt.plot(marker="o").
fig = px.line(weekly,
    x="week",
    y=["average_score", "top_score", "low_score"],
    title="Weekly Score Trend",
    markers=True,
    labels={"week": "Week", "value": "Score", "variable": "Metric"}
)

# update_layout() modifies chart-level properties like title font,
# legend position, background color, and axis labels all in one call.
fig.update_layout(
    title_font_size=16,
    hovermode="x unified"   # shows all three lines' values in one tooltip
)

fig.show()

# PART 2: px.scatter : interactive scatter with hover details
# hover_name= sets which column appears as the bold title in the tooltip.
# hover_data= adds extra fields below it.
# color= and size= work exactly like Seaborn's hue= and size=,
# but the result is interactive : we can click legend items to
# hide/show specific cities, and hover to see exact student details.
fig2 = px.scatter(students,
    x="study_hours",
    y="score",
    color="city",
    size="sleep_hours",
    hover_name="name",      # bold label at top of tooltip
    hover_data={            # extra fields shown in tooltip
        "study_hours": True,
        "sleep_hours": True,
        "score":       True,
        "attendance":  True,
        "grade":       True,
        "city":        False  # city already shown as color, hide from tooltip
    },
    color_discrete_map={
        "Dhangadhi": "goldenrod",
        "Kathmandu": "steelblue",
        "Pokhara":   "coral",
        "Butwal":    "mediumseagreen"
    },
    title="Study Hours vs Score (Interactive)",
    labels={
        "study_hours": "Study Hours per Day",
        "score":       "Score",
        "sleep_hours": "Sleep Hours"
    }
)

fig2.update_layout(title_font_size=16)
fig2.show()

# PART 3: px.bar : interactive bar chart
# barmode="group" places bars side by side per student.
# color_discrete_sequence= sets the color per bar group manually.
fig3 = px.bar(students,
    x="name",
    y=["score", "attendance"],
    barmode="group",
    hover_data={"grade": True},
    title="Score and Attendance per Student",
    labels={"name": "Student", "value": "Value", "variable": "Metric"}
)

fig3.update_layout(title_font_size=16)
fig3.show()

# PART 4: saving a Plotly chart as a static PNG
# write_image() exports the chart as a static file.
# requires: pip install kaleido
# WHY THIS MATTERS: interactive charts live in the browser,
# but reports and tweets need a static image. write_image()
# gives us the best of both : build interactively, export statically.
try:
    fig2.write_image("scatter_interactive.png", scale=2)
    print("Saved scatter_interactive.png")
except Exception as e:
    print(f"Install kaleido to save static images: pip install kaleido\n{e}")