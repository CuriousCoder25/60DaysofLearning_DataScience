import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score

plt.ion()
sns.set_theme(style="whitegrid", palette="muted")

np.random.seed(42)
n = 30

passengers = pd.DataFrame({
    "name":   [f"Passenger_{i}" for i in range(1, n+1)],
    "age":    np.random.randint(5, 70, n),
    "fare":   np.round(np.random.uniform(7, 250, n), 2),
    "pclass": np.random.choice([1, 2, 3], n, p=[0.25, 0.25, 0.5]),
    "sex":    np.random.choice(["male", "female"], n)
})

survival_prob = (
    0.3
    + (passengers["sex"] == "female") * 0.4
    + (passengers["pclass"] == 1) * 0.25
    + (passengers["pclass"] == 2) * 0.10
    - (passengers["age"] > 50) * 0.15
)
survival_prob = survival_prob.clip(0.05, 0.95)
passengers["survived"] = np.random.binomial(1, survival_prob)
passengers["sex_encoded"] = (passengers["sex"] == "female").astype(int)

X = passengers[["age", "fare", "pclass", "sex_encoded"]]
y = passengers["survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print("=" * 50)
print("  Decision Trees : Day 54")
print("=" * 50)

# ---- PART 1: how decision trees work, conceptually ----
# a decision tree asks a SERIES of yes/no questions about features,
# splitting the data at each step to separate classes as cleanly
# as possible. example: "is sex_encoded <= 0.5?" splits male/female,
# then "is pclass <= 1.5?" splits first class from the rest, and so on.
# WHY THIS MATTERS: unlike logistic regression, which fits a single
# smooth boundary, trees can carve out IRREGULAR, non-linear boundaries,
# and every decision is human-readable, we can literally read the rules.

# NOTE: decision trees do NOT require feature scaling.
# they split based on threshold comparisons (is X <= value?),
# which are unaffected by the scale of the feature.
# this is a genuine advantage over logistic regression.
tree_model = DecisionTreeClassifier(max_depth=3, random_state=42)
tree_model.fit(X_train, y_train)

y_pred_tree = tree_model.predict(X_test)

print(f"\nDecision Tree trained on {len(X_train)} samples (no scaling needed)\n")

# ---- PART 2: visualizing the tree itself ----
# plot_tree() draws the actual decision structure the model learned.
# each box shows: the splitting condition, gini impurity (how mixed
# the classes are), sample count, and the class distribution.
# WHY THIS MATTERS: this is one of the FEW ML models we can fully
# read and explain to a non-technical person, every decision is visible.
plt.figure(figsize=(16, 8), num="Decision Tree Structure")
plot_tree(tree_model,
    feature_names=X.columns,
    class_names=["Died", "Survived"],
    filled=True,       # colors boxes by predicted class
    rounded=True,
    fontsize=9
)
plt.title("Decision Tree (max_depth=3)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show(block=False)

# ---- PART 3: feature importance ----
# .feature_importances_ tells us how much each feature contributed
# to reducing impurity across all splits in the tree.
# higher value = more useful for making predictions.
importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": tree_model.feature_importances_
}).sort_values("importance", ascending=False)

print(f"Feature importances:\n{importance_df.to_string(index=False)}\n")

plt.figure(figsize=(7, 4), num="Feature Importance")
plt.barh(importance_df["feature"], importance_df["importance"],
    color="steelblue", edgecolor="white")
plt.title("Feature Importance (Decision Tree)", fontweight="bold")
plt.xlabel("Importance")
plt.tight_layout()
plt.show(block=False)

# ---- PART 4: tuning max_depth ----
# max_depth controls how many questions the tree can ask before
# making a final decision. WHY THIS MATTERS: too shallow = underfitting
# (misses real patterns), too deep = OVERFITTING (memorizes training
# data noise instead of learning general rules that work on new data).
depths = range(1, 10)
train_accuracies = []
test_accuracies = []

for depth in depths:
    dt = DecisionTreeClassifier(max_depth=depth, random_state=42)
    dt.fit(X_train, y_train)
    train_accuracies.append(accuracy_score(y_train, dt.predict(X_train)))
    test_accuracies.append(accuracy_score(y_test, dt.predict(X_test)))

plt.figure(figsize=(8, 5), num="Max Depth Tuning")
plt.plot(depths, train_accuracies, marker="o", label="Train Accuracy", color="steelblue")
plt.plot(depths, test_accuracies, marker="o", label="Test Accuracy", color="coral")
plt.title("Overfitting Check: Train vs Test Accuracy by Depth", fontweight="bold")
plt.xlabel("max_depth")
plt.ylabel("Accuracy")
plt.legend()
plt.tight_layout()
plt.show(block=False)

print("Depth tuning results:")
for d, tr, te in zip(depths, train_accuracies, test_accuracies):
    gap = tr - te
    flag = "  <- overfitting gap growing" if gap > 0.15 else ""
    print(f"  depth={d}: train={tr:.3f}, test={te:.3f}, gap={gap:.3f}{flag}")

# ---- PART 5: comparing decision tree vs logistic regression ----
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

log_model = LogisticRegression()
log_model.fit(X_train_scaled, y_train)
y_pred_log = log_model.predict(X_test_scaled)

tree_acc = accuracy_score(y_test, y_pred_tree)
tree_f1  = f1_score(y_test, y_pred_tree, zero_division=0)
log_acc  = accuracy_score(y_test, y_pred_log)
log_f1   = f1_score(y_test, y_pred_log, zero_division=0)

comparison = pd.DataFrame({
    "model": ["Decision Tree", "Logistic Regression"],
    "accuracy": [tree_acc, log_acc],
    "f1_score": [tree_f1, log_f1]
})

print(f"\nModel comparison:\n{comparison.to_string(index=False)}\n")

plt.figure(figsize=(7, 5), num="Model Comparison")
x_pos = np.arange(2)
width = 0.35
plt.bar(x_pos - width/2, comparison["accuracy"], width, label="Accuracy", color="steelblue")
plt.bar(x_pos + width/2, comparison["f1_score"], width, label="F1 Score", color="coral")
plt.xticks(x_pos, comparison["model"])
plt.title("Decision Tree vs Logistic Regression", fontweight="bold")
plt.ylabel("Score")
plt.legend()
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("tree_vs_logistic.png", dpi=150, bbox_inches="tight")
plt.show(block=False)

print(f"Saved tree_vs_logistic.png")

plt.ioff()
plt.show()