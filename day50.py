import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

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
                    83, 94, 77, 88, 96, 68, 85, 93, 79, 91]
})

X = students[["study_hours", "sleep_hours", "attendance", "assignments"]]
y = students["score"]

# split first, THEN scale.
# WHY ORDER MATTERS: if we scale before splitting, the scaler
# sees the test set values during fit() and leaks information
# about the test set into the training process. always split first.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # fit on train only
X_test_scaled  = scaler.transform(X_test)         # transform test using train's stats

print("=" * 50)
print("  Linear Regression : Day 50")
print("=" * 50)

#  PART 1: what linear regression actually does 
# LINEAR REGRESSION fits a line (or hyperplane in multiple dimensions)
# that minimizes the sum of squared errors between predicted and actual values.
# the formula is: score = intercept + (w1 * study_hours) + (w2 * sleep_hours) + ...
# the model learns the WEIGHTS (w1, w2...) that make this equation
# as accurate as possible on the training data.
# WHY THIS MATTERS: this is the simplest possible ML model.
# understanding it deeply makes every other model easier to grasp.
model = LinearRegression()

# .fit() is where learning happens : the model adjusts its weights
# to minimize prediction errors on the training data.
model.fit(X_train_scaled, y_train)

print(f"\nModel trained on {len(X_train)} samples\n")

#  PART 2: interpreting the coefficients 
# .intercept_ is the baseline prediction when all features are 0.
# .coef_ are the learned weights for each feature.
# because we StandardScaled our features, coefficients are
# directly comparable : a larger absolute coefficient means
# that feature has MORE influence on the predicted score.
coef_df = pd.DataFrame({
    "feature":     X.columns,
    "coefficient": model.coef_
}).sort_values("coefficient", ascending=False)

print(f"Intercept (baseline prediction) : {model.intercept_:.2f}")
print(f"\nFeature coefficients (scaled):\n{coef_df.to_string(index=False)}\n")
print("Positive = increases score, Negative = decreases score")
print("Larger absolute value = stronger influence on prediction\n")

#  PART 3: making predictions 
# .predict() applies the learned formula to new data.
# we pass X_test_scaled (NOT X_test) because the model was
# trained on scaled data : raw values would give wrong predictions.
y_pred = model.predict(X_test_scaled)

print(f"Predictions vs actual (test set):")
print(f"{'Student':<10} {'Actual':>8} {'Predicted':>10} {'Error':>8}")
print("-" * 40)
for i, (actual, predicted) in enumerate(zip(y_test, y_pred)):
    error = actual - predicted
    name = students.loc[y_test.index[i], "name"]
    print(f"{name:<10} {actual:>8.1f} {predicted:>10.1f} {error:>8.1f}")

#  PART 4: visualizing predictions 
fig, axes = plt.subplots(1, 2, figsize=(13, 5), num="Linear Regression")

# left: predicted vs actual scatter
# a perfect model would have all dots on the red diagonal line.
# dots above the line = model underpredicted.
# dots below the line = model overpredicted.
axes[0].scatter(y_test, y_pred, color="steelblue", s=80, alpha=0.8)
min_val = min(y_test.min(), y_pred.min()) - 2
max_val = max(y_test.max(), y_pred.max()) + 2
axes[0].plot([min_val, max_val], [min_val, max_val],
    color="red", linestyle="--", linewidth=1.5, label="Perfect prediction")
axes[0].set_title("Predicted vs Actual", fontweight="bold")
axes[0].set_xlabel("Actual Score")
axes[0].set_ylabel("Predicted Score")
axes[0].legend()

# right: feature importance via coefficients
colors = ["steelblue" if c > 0 else "coral" for c in coef_df["coefficient"]]
axes[1].barh(coef_df["feature"], coef_df["coefficient"],
    color=colors, edgecolor="white")
axes[1].axvline(x=0, color="black", linewidth=0.8)
axes[1].set_title("Feature Coefficients", fontweight="bold")
axes[1].set_xlabel("Coefficient Value")

plt.suptitle("Linear Regression Results", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show(block=False)

#  PART 5: predicting a NEW student 
# this is the actual use case: a student we've never seen before.
# we must scale using the SAME scaler fitted on training data :
# never refit the scaler on new data.
new_student = pd.DataFrame({
    "study_hours": [6],
    "sleep_hours": [7],
    "attendance":  [88],
    "assignments": [9]
})

new_scaled = scaler.transform(new_student)
prediction = model.predict(new_scaled)[0]
print(f"\nNew student prediction:")
print(f"  study_hours=6, sleep_hours=7, attendance=88, assignments=9")
print(f"  Predicted score: {prediction:.1f}")

plt.ioff()
plt.show()