import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder

plt.ion()
sns.set_theme(style="whitegrid", palette="muted")

students = pd.DataFrame({
    "name":        ["Gaurav", "Alice", "Pino", "Diana", "Evren",
                    "Frank", "Grace", "Henry", "Iris", "Jack"],
    "study_hours": [4, 6, 3, 7, 5, 2, 8, 4, 6, 3],
    "sleep_hours": [7, 6, 5, 8, 7, 4, 8, 6, 7, 5],
    "score":       [88, 92, 75, 95, 81, 65, 97, 80, 90, 70],
    "attendance":  [85, 90, 70, 95, 88, 60, 98, 82, 91, 72],
    "city":        ["Dhangadhi", "Pokhara", "Kathmandu", "Butwal", "Pokhara",
                    "Butwal", "Kathmandu", "Pokhara", "Butwal", "Kathmandu"],
    "grade":       ["B", "A", "C", "A", "B", "F", "A", "B", "A", "C"]
})

numeric_cols = ["study_hours", "sleep_hours", "score", "attendance"]
X_numeric = students[numeric_cols].copy()

print("=" * 50)
print("  Feature Preprocessing : Day 48")
print("=" * 50)
print(f"\nOriginal numeric features:\n{X_numeric}\n")

# WHY PREPROCESSING MATTERS: ML models compute distances and
# weighted sums between feature values. if "attendance" ranges
# 60-98 and "study_hours" ranges 2-8, the model will wrongly
# treat attendance as more important just because its numbers
# are bigger. scaling puts every feature on equal footing.

#   PART 1: MinMaxScaler  
# formula: (x - min) / (max - min)
# squashes every value into the range [0, 1].
# we derived this formula manually back on Day 20.
# NOW sklearn does it automatically, but we know what's inside.
# WHEN TO USE: when we know the data has a fixed range and
# outliers are not a problem. pixel values (0-255) are a classic case.
minmax = MinMaxScaler()

# fit() learns the min and max from the data.
# transform() applies the formula using those learned values.
# fit_transform() does both in one step : only use on TRAINING data.
X_minmax = minmax.fit_transform(X_numeric)
X_minmax_df = pd.DataFrame(X_minmax, columns=numeric_cols)
print(f"After MinMaxScaler (range 0-1):\n{X_minmax_df.round(3)}\n")

# verify the range
print(f"Min after MinMax: {X_minmax_df.min().values}")
print(f"Max after MinMax: {X_minmax_df.max().values}\n")

#   PART 2: StandardScaler  
# formula: (x - mean) / std
# centers the data around 0 with a standard deviation of 1.
# result is called a "z-score" : how many standard deviations
# away from the mean each value is.
# WHEN TO USE: when data roughly follows a normal distribution
# and outliers exist. most ML algorithms prefer this over MinMax
# because it doesn't compress outliers into corners of [0,1].
standard = StandardScaler()
X_standard = standard.fit_transform(X_numeric)
X_standard_df = pd.DataFrame(X_standard, columns=numeric_cols)
print(f"After StandardScaler (mean=0, std=1):\n{X_standard_df.round(3)}\n")

# verify mean is ~0 and std is ~1 for each column
print(f"Mean after Standard: {X_standard_df.mean().round(6).values}")
print(f"Std  after Standard: {X_standard_df.std().round(3).values}\n")

#   PART 3: visualizing the effect of scaling  
# this is the clearest way to see WHAT scaling actually does
# to the distribution shape and the relative column ranges.
fig, axes = plt.subplots(1, 3, figsize=(15, 4), num="Scaling Comparison")

# original
X_numeric.boxplot(ax=axes[0])
axes[0].set_title("Original (unscaled)", fontweight="bold")
axes[0].set_ylabel("Value")

# MinMax scaled
X_minmax_df.boxplot(ax=axes[1])
axes[1].set_title("MinMaxScaler [0, 1]", fontweight="bold")

# Standard scaled
X_standard_df.boxplot(ax=axes[2])
axes[2].set_title("StandardScaler [z-scores]", fontweight="bold")

plt.suptitle("Effect of Scaling on Feature Distributions",
    fontsize=13, fontweight="bold")
plt.tight_layout()
plt.show(block=False)

#   PART 4: OneHotEncoder : handling categorical columns  
# ML models only understand NUMBERS, not strings like "Kathmandu"
# or "Grade A". OneHotEncoder converts each category into its own
# binary (0 or 1) column. one column per unique category value.
# WHY THIS MATTERS: we can't just assign numbers (Kathmandu=1,
# Pokhara=2) because that implies an ordering that doesn't exist.
# OneHot treats each category as completely independent.
encoder = OneHotEncoder(sparse_output=False)   # sparse_output=False returns a dense array

# reshape needed because OneHotEncoder expects 2D input
city_encoded = encoder.fit_transform(students[["city"]])
city_encoded_df = pd.DataFrame(
    city_encoded,
    columns=encoder.get_feature_names_out(["city"])
)
print(f"After OneHotEncoder (city column):\n{city_encoded_df}\n")

#   PART 5: assembling the full preprocessed feature matrix  
# in a real pipeline we'd preprocess numeric and categorical columns
# separately then combine them into one final feature matrix ready
# for a model. this is what we'll wrap into a sklearn Pipeline on Day 58.
X_final = pd.concat([
    X_standard_df,           # scaled numeric features
    city_encoded_df,         # one-hot encoded city
    pd.get_dummies(students["grade"], prefix="grade")  # grade encoded
], axis=1)

print(f"Final preprocessed feature matrix shape: {X_final.shape}")
print(f"\nFirst 3 rows:\n{X_final.head(3).round(3)}")

plt.ioff()
plt.show()