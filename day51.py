import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

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

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

model = LinearRegression()
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

print("=" * 50)
print("  Regression Evaluation : Day 51")
print("=" * 50)

# ---- PART 1: the three core regression metrics ----

# MAE: Mean Absolute Error
# average of absolute differences between predicted and actual.
# easy to interpret: "on average, predictions are off by X points."
# not penalizing large errors extra : every error is treated equally.
mae = mean_absolute_error(y_test, y_pred)
print(f"\nMAE  : {mae:.2f}")
print(f"       on average predictions are off by {mae:.2f} score points")

# MSE: Mean Squared Error
# average of SQUARED differences. squaring penalizes large errors
# much more than small ones. a prediction off by 10 contributes
# 100 to MSE, while one off by 1 only contributes 1.
# WHY THIS MATTERS: if large errors are especially costly in our
# use case, MSE is more sensitive to them than MAE.
mse = mean_squared_error(y_test, y_pred)
print(f"\nMSE  : {mse:.2f}")
print(f"       hard to interpret directly because units are squared")

# RMSE: Root Mean Squared Error
# square root of MSE, brings units back to the original scale.
# like MAE but penalizes large errors more.
# this is the most commonly reported regression metric in practice.
rmse = np.sqrt(mse)
print(f"\nRMSE : {rmse:.2f}")
print(f"       typical prediction error is around {rmse:.2f} score points")

# R²: Coefficient of Determination
# measures how much of the variance in y our model explains.
# R²=1.0 means perfect predictions, R²=0.0 means the model is
# no better than just predicting the mean every time,
# R²<0 means the model is WORSE than predicting the mean.
# WHY THIS MATTERS: R² gives a normalized 0-1 score that's
# comparable across different datasets, unlike MAE/RMSE which
# depend on the scale of y.
r2 = r2_score(y_test, y_pred)
print(f"\nR²   : {r2:.4f}")
print(f"       the model explains {r2*100:.1f}% of score variance\n")

# ---- PART 2: residuals ----
# RESIDUAL = actual - predicted.
# if the model is good, residuals should be:
# 1. centered around 0 (no systematic bias)
# 2. randomly scattered (no pattern)
# if residuals show a pattern, the model is missing something.
residuals = y_test.values - y_pred

print(f"Residuals (actual - predicted):")
print(f"{'Student':<10} {'Actual':>8} {'Predicted':>10} {'Residual':>10}")
print("-" * 42)
for i, (actual, predicted, resid) in enumerate(zip(y_test, y_pred, residuals)):
    name = students.loc[y_test.index[i], "name"]
    print(f"{name:<10} {actual:>8.1f} {predicted:>10.1f} {resid:>10.1f}")

print(f"\nMean residual    : {residuals.mean():.4f}  (should be ~0)")
print(f"Residual std     : {residuals.std():.2f}")

# ---- PART 3: visualizing model quality ----
fig, axes = plt.subplots(1, 3, figsize=(16, 5), num="Regression Evaluation")

# left: predicted vs actual
# dots should cluster tightly around the diagonal red line.
# dots far from the line = large errors.
axes[0].scatter(y_test, y_pred, color="steelblue", s=80, alpha=0.8)
min_val = min(y_test.min(), y_pred.min()) - 2
max_val = max(y_test.max(), y_pred.max()) + 2
axes[0].plot([min_val, max_val], [min_val, max_val],
    color="red", linestyle="--", linewidth=1.5, label="Perfect fit")
for i, name in enumerate(students.loc[y_test.index, "name"]):
    axes[0].annotate(name,
        (y_test.values[i], y_pred[i]),
        textcoords="offset points", xytext=(5, 5), fontsize=7)
axes[0].set_title(f"Predicted vs Actual\nR²={r2:.3f}", fontweight="bold")
axes[0].set_xlabel("Actual Score")
axes[0].set_ylabel("Predicted Score")
axes[0].legend(fontsize=8)

# middle: residual plot
# dots should be randomly scattered around the horizontal 0 line.
# any curved or fanning pattern suggests the model needs improvement.
axes[1].scatter(y_pred, residuals, color="coral", s=80, alpha=0.8)
axes[1].axhline(y=0, color="red", linestyle="--", linewidth=1.5)
axes[1].set_title("Residual Plot\n(random scatter = good)", fontweight="bold")
axes[1].set_xlabel("Predicted Score")
axes[1].set_ylabel("Residual (Actual - Predicted)")

# right: residual distribution
# should look roughly bell-shaped and centered on 0.
# skew or heavy tails suggest systematic prediction errors.
sns.histplot(residuals, kde=True, color="mediumseagreen", bins=6, ax=axes[2])
axes[2].axvline(x=0, color="red", linestyle="--", linewidth=1.5)
axes[2].set_title("Residual Distribution\n(centered on 0 = good)", fontweight="bold")
axes[2].set_xlabel("Residual")

plt.suptitle("Regression Model Evaluation", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show(block=False)

# ---- PART 4: what a BAD fit looks like ----
# deliberately create a bad model: predict using ONLY sleep_hours,
# which has very low correlation with score. this shows what
# high MSE and low R² actually look like visually.
bad_model = LinearRegression()
X_bad_train = X_train_scaled[:, 1].reshape(-1, 1)  # sleep_hours only
X_bad_test  = X_test_scaled[:, 1].reshape(-1, 1)

bad_model.fit(X_bad_train, y_train)
y_bad_pred = bad_model.predict(X_bad_test)

bad_r2   = r2_score(y_test, y_bad_pred)
bad_rmse = np.sqrt(mean_squared_error(y_test, y_bad_pred))

fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5), num="Good vs Bad Fit")

# good model
axes2[0].scatter(y_test, y_pred, color="steelblue", s=80, alpha=0.8)
axes2[0].plot([min_val, max_val], [min_val, max_val],
    color="red", linestyle="--", linewidth=1.5)
axes2[0].set_title(f"Good Model (all features)\nR²={r2:.3f}, RMSE={rmse:.2f}",
    fontweight="bold")
axes2[0].set_xlabel("Actual Score")
axes2[0].set_ylabel("Predicted Score")

# bad model
axes2[1].scatter(y_test, y_bad_pred, color="coral", s=80, alpha=0.8)
axes2[1].plot([min_val, max_val], [min_val, max_val],
    color="red", linestyle="--", linewidth=1.5)
axes2[1].set_title(f"Bad Model (sleep_hours only)\nR²={bad_r2:.3f}, RMSE={bad_rmse:.2f}",
    fontweight="bold")
axes2[1].set_xlabel("Actual Score")
axes2[1].set_ylabel("Predicted Score")

plt.suptitle("Good vs Bad Fit : Same Diagonal, Different Scatter",
    fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("regression_evaluation.png", dpi=150, bbox_inches="tight")
plt.show(block=False)

print(f"\nGood model  : R²={r2:.3f}, RMSE={rmse:.2f}")
print(f"Bad model   : R²={bad_r2:.3f}, RMSE={bad_rmse:.2f}")
print(f"\nSaved regression_evaluation.png")

plt.ioff()
plt.show()