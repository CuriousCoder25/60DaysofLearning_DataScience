import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score,
    recall_score, f1_score, classification_report
)

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

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

print("=" * 50)
print("  Classification Metrics — Day 53")
print("=" * 50)

# ---- PART 1: the confusion matrix ----
# a confusion matrix breaks predictions into 4 categories:
# TRUE POSITIVE  (TP): predicted survived, actually survived
# TRUE NEGATIVE  (TN): predicted died, actually died
# FALSE POSITIVE (FP): predicted survived, actually died     (a false alarm)
# FALSE NEGATIVE (FN): predicted died, actually survived     (a missed case)
# WHY THIS MATTERS: accuracy alone hides WHICH kind of mistake
# the model makes. two models with the same accuracy can fail
# in very different, and very differently costly, ways.
cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:\n{cm}\n")

tn, fp, fn, tp = cm.ravel()
print(f"True Negatives  (correctly predicted died)     : {tn}")
print(f"False Positives (predicted survived, died)     : {fp}")
print(f"False Negatives (predicted died, survived)     : {fn}")
print(f"True Positives  (correctly predicted survived) : {tp}\n")

# visualize the confusion matrix as a heatmap
plt.figure(figsize=(6, 5), num="Confusion Matrix")
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
    xticklabels=["Predicted: Died", "Predicted: Survived"],
    yticklabels=["Actual: Died", "Actual: Survived"],
    cbar=False, linewidths=1, linecolor="white")
plt.title("Confusion Matrix", fontweight="bold")
plt.tight_layout()
plt.show(block=False)

# ---- PART 2: accuracy ----
# accuracy = (TP + TN) / total
# simplest metric: what fraction of predictions were correct overall.
# WHY IT CAN MISLEAD: on imbalanced data (say 90% died, 10% survived),
# a model that ALWAYS predicts "died" gets 90% accuracy while being
# completely useless for identifying survivors.
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy  : {accuracy:.3f}  ({accuracy*100:.1f}% of predictions correct)\n")

# ---- PART 3: precision ----
# precision = TP / (TP + FP)
# "of everyone we PREDICTED survived, how many actually did?"
# HIGH PRECISION matters when false positives are costly.
# example: predicting spam email, a false positive means a real
# email gets deleted, which is worse than missing one spam email.
precision = precision_score(y_test, y_pred, zero_division=0)
print(f"Precision : {precision:.3f}  (of predicted survivors, {precision*100:.1f}% actually survived)\n")

# ---- PART 4: recall ----
# recall = TP / (TP + FN)
# "of everyone who ACTUALLY survived, how many did we catch?"
# HIGH RECALL matters when false negatives are costly.
# example: cancer detection, a false negative means a sick patient
# gets told they're healthy, which is far worse than a false alarm.
recall = recall_score(y_test, y_pred, zero_division=0)
print(f"Recall    : {recall:.3f}  (of actual survivors, we correctly identified {recall*100:.1f}%)\n")

# ---- PART 5: F1 score ----
# F1 = 2 * (precision * recall) / (precision + recall)
# the HARMONIC MEAN of precision and recall, not a simple average.
# harmonic mean punishes extreme imbalance, a model with precision=1.0
# and recall=0.1 gets a LOW F1, not a mediocre 0.55 average would suggest.
# WHY THIS MATTERS: F1 is the go-to single number when we care about
# BOTH precision and recall roughly equally, and classes are imbalanced.
f1 = f1_score(y_test, y_pred, zero_division=0)
print(f"F1 Score  : {f1:.3f}  (balances precision and recall)\n")

# ---- PART 6: full classification report ----
# classification_report() computes all of the above automatically,
# broken down PER CLASS, plus weighted averages across classes.
print("Full classification report:")
print(classification_report(y_test, y_pred,
    target_names=["Died", "Survived"], zero_division=0))

# ---- PART 7: precision-recall tradeoff visualization ----
# threshold controls the cutoff for classifying as class 1.
# default threshold is 0.5, but shifting it trades precision for recall.
# lower threshold -> more predicted positives -> higher recall, lower precision
# higher threshold -> fewer predicted positives -> higher precision, lower recall
y_proba = model.predict_proba(X_test_scaled)[:, 1]
thresholds = np.arange(0.1, 1.0, 0.05)

precisions, recalls, f1s = [], [], []
for t in thresholds:
    y_pred_t = (y_proba >= t).astype(int)
    precisions.append(precision_score(y_test, y_pred_t, zero_division=0))
    recalls.append(recall_score(y_test, y_pred_t, zero_division=0))
    f1s.append(f1_score(y_test, y_pred_t, zero_division=0))

plt.figure(figsize=(8, 5), num="Precision Recall Tradeoff")
plt.plot(thresholds, precisions, marker="o", label="Precision", color="steelblue")
plt.plot(thresholds, recalls, marker="o", label="Recall", color="coral")
plt.plot(thresholds, f1s, marker="o", label="F1 Score", color="mediumseagreen")
plt.axvline(x=0.5, color="gray", linestyle="--", linewidth=1, label="Default threshold")
plt.title("Precision-Recall Tradeoff Across Thresholds", fontweight="bold")
plt.xlabel("Classification Threshold")
plt.ylabel("Score")
plt.legend()
plt.tight_layout()
plt.savefig("classification_metrics.png", dpi=150, bbox_inches="tight")
plt.show(block=False)

print(f"\nSaved classification_metrics.png")

plt.ioff()
plt.show()