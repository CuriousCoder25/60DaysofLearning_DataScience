import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

plt.ion()
sns.set_theme(style="whitegrid", palette="muted")

students = pd.DataFrame({
    "name":        ["Gaurav", "Alice", "Pino", "Diana", "Evren",
                    "Frank", "Grace", "Henry", "Iris", "Jack",
                    "Karen", "Leo", "Mia", "Noah", "Olivia",
                    "Paul", "Quinn", "Rita", "Sam", "Tina"],
    "study_hours": [4, 6, 3, 7, 5, 2, 8, 4, 6, 3,
                    5, 7, 4, 6, 8, 3, 5, 7, 4, 6],
    "sleep_hours": [7, 6, 5, 8, 7, 4, 8, 6, 7, 5,
                    6, 8, 5, 7, 8, 5, 6, 7, 6, 8],
    "attendance":  [85, 90, 70, 95, 88, 60, 98, 82, 91, 72,
                    80, 93, 75, 88, 96, 68, 84, 92, 78, 90],
    "assignments": [9, 10, 7, 10, 8, 5, 10, 8, 9, 6,
                    8, 10, 7, 9, 10, 6, 8, 9, 7, 10],
    "score":       [88, 92, 75, 95, 81, 65, 97, 80, 90, 70,
                    83, 94, 77, 88, 96, 68, 85, 93, 79, 91],
    "grade":       ["B", "A", "C", "A", "B", "F", "A", "B", "A", "C",
                    "B", "A", "C", "B", "A", "F", "B", "A", "C", "A"]
})

# FEATURES (X) and TARGET (y):
# X = the input columns the model learns FROM.
# y = the output column the model learns TO PREDICT.
# we drop "name" (not a useful feature) and "grade"
# (derived from score, would leak the answer to the model).
X = students[["study_hours", "sleep_hours", "attendance", "assignments"]]
y = students["score"]

print("=" * 50)
print("  Train/Test Split : Day 49")
print("=" * 50)
print(f"\nFull dataset    : {X.shape[0]} samples, {X.shape[1]} features")
print(f"Target variable : score (continuous, range {y.min()}-{y.max()})\n")

# WHY WE SPLIT: if we train a model on ALL the data and then test
# it on the SAME data, it will always look accurate : it already
# memorized those exact values. this is called OVERFITTING.
# a test set the model has NEVER seen during training gives us
# an honest estimate of how well it generalizes to new data.

# train_test_split() randomly shuffles then splits the data.
# test_size=0.2 means 20% goes to test, 80% stays for training.
# random_state= fixes the random seed so the split is identical
# every run : without this, each run gives a different split
# and our accuracy scores become unreproducible.
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print(f"Training set    : {X_train.shape[0]} samples ({X_train.shape[0]/len(X)*100:.0f}%)")
print(f"Test set        : {X_test.shape[0]} samples ({X_test.shape[0]/len(X)*100:.0f}%)\n")

# verify the indices to see which rows went where
print(f"Training indices : {sorted(X_train.index.tolist())}")
print(f"Test indices     : {sorted(X_test.index.tolist())}\n")

# WHY RANDOM_STATE MATTERS: run without it and the split changes every time
X_train_r1, X_test_r1, _, _ = train_test_split(X, y, test_size=0.2, random_state=1)
X_train_r2, X_test_r2, _, _ = train_test_split(X, y, test_size=0.2, random_state=2)

print(f"Split with random_state=1  test indices: {sorted(X_test_r1.index.tolist())}")
print(f"Split with random_state=2  test indices: {sorted(X_test_r2.index.tolist())}")
print(f"Split with random_state=42 test indices: {sorted(X_test.index.tolist())}")
print(f"(Different seeds = different splits every time)\n")

# ---- STRATIFIED SPLIT ----
# stratify= ensures the CLASS DISTRIBUTION in train and test sets
# matches the original dataset. without it, by pure chance the test
# set might end up with all "A" students and no "F" students,
# giving a misleading picture of model performance.
# stratify= is essential for CLASSIFICATION problems (predicting grades)
# less critical for REGRESSION problems (predicting numeric scores).
X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(
    X, students["grade"],   # use grade as target for this demo
    test_size=0.2,
    random_state=42,
    stratify=students["grade"]   # preserve grade distribution
)

print(f"Grade distribution in full dataset:\n{students['grade'].value_counts().sort_index()}\n")
print(f"Grade distribution in train set:\n{y_train_s.value_counts().sort_index()}\n")
print(f"Grade distribution in test set:\n{y_test_s.value_counts().sort_index()}\n")

# ---- VISUALIZING THE SPLIT ----
fig, axes = plt.subplots(1, 2, figsize=(12, 4), num="Train Test Split")

# left: show which rows ended up in train vs test
colors = ["steelblue" if i in X_train.index else "coral"
          for i in students.index]
axes[0].bar(students["name"], students["score"], color=colors, edgecolor="white")
axes[0].set_title("Train (blue) vs Test (coral) split", fontweight="bold")
axes[0].set_xlabel("Student")
axes[0].set_ylabel("Score")
axes[0].tick_params(axis="x", rotation=45)

# add a legend manually
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor="steelblue", label="Train"),
                   Patch(facecolor="coral", label="Test")]
axes[0].legend(handles=legend_elements)

# right: score distribution comparison between train and test
axes[1].hist(y_train, bins=6, alpha=0.6, color="steelblue", label=f"Train (n={len(y_train)})")
axes[1].hist(y_test,  bins=6, alpha=0.6, color="coral",     label=f"Test  (n={len(y_test)})")
axes[1].set_title("Score Distribution: Train vs Test", fontweight="bold")
axes[1].set_xlabel("Score")
axes[1].set_ylabel("Count")
axes[1].legend()

plt.tight_layout()
plt.show(block=False)

# ---- SUMMARY ----
print("=" * 50)
print("  Split Summary")
print("=" * 50)
print(f"  Train mean score : {y_train.mean():.2f}")
print(f"  Test  mean score : {y_test.mean():.2f}")
print(f"  Train std        : {y_train.std():.2f}")
print(f"  Test  std        : {y_test.std():.2f}")
print(f"\n  Both sets look similar in distribution.")
print(f"  Model will train on {len(X_train)} rows, be judged on {len(X_test)}.")

plt.ioff()
plt.show()