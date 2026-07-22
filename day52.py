import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

plt.ion()
sns.set_theme(style="whitegrid", palette="muted")

# ------------------------------------------------------------
# DAY 52 : LOGISTIC REGRESSION
#
# Yesterday we predicted continuous values such as exam scores.
# That was a REGRESSION problem.
#
# Today the output is completely different.
#
# Instead of predicting:
#     87.4
#     91.8
#     76.2
#
# we predict one of two classes:
#
#     Pass
#     Fail
#
# or numerically,
#
#     1 = Pass
#     0 = Fail
#
# This type of problem is called Binary Classification.
# ------------------------------------------------------------

students = pd.DataFrame({

    "name":[
        "Gaurav","Alice","Pino","Diana","Evren",
        "Frank","Grace","Henry","Iris","Jack",
        "Karen","Leo","Mia","Noah","Olivia",
        "Paul","Quinn","Rita","Sam","Tina"
    ],

    "study_hours":[
        4,6,3,7,5,
        2,8,4,6,3,
        5,7,4,6,8,
        3,5,7,4,6
    ],

    "sleep_hours":[
        7,6,5,8,7,
        4,8,6,7,5,
        6,8,5,7,8,
        5,6,7,6,8
    ],

    "attendance":[
        85,90,70,95,88,
        60,98,82,91,72,
        80,93,75,88,96,
        68,84,92,78,90
    ],

    "assignments":[
        9,10,7,10,8,
        5,10,8,9,6,
        8,10,7,9,10,
        6,8,9,7,10
    ],

    # Binary target
    # 1 = Pass
    # 0 = Fail
    "passed":[
        1,1,0,1,1,
        0,1,1,1,0,
        1,1,0,1,1,
        0,1,1,0,1
    ]

})

print("="*55)
print(" Logistic Regression : Binary Classification")
print("="*55)

print(f"\nDataset:\n")
print(students)

# ------------------------------------------------------------
# WHY NOT LINEAR REGRESSION?
#
# Linear Regression predicts any real number.
#
# Example:
#
#     -0.82
#      1.64
#      2.13
#
# None of these make sense when the answer should ONLY be
#
#      0
#      1
#
# Logistic Regression solves this by converting the prediction
# into a probability between 0 and 1 using the Sigmoid function.
# ------------------------------------------------------------

# ------------------------------------------------------------
# THE SIGMOID FUNCTION
#
#            1
#  ----------------------
#   1 + e^(-x)
#
# Large negative x  -> probability near 0
#
# x = 0            -> probability = 0.5
#
# Large positive x -> probability near 1
#
# WHY THIS MATTERS:
#
# Instead of predicting impossible values such as
#
#     2.4
#     -1.8
#
# every prediction becomes a probability.
# ------------------------------------------------------------

x = np.linspace(-10,10,400)

sigmoid = 1/(1+np.exp(-x))

plt.figure(figsize=(8,5),num="Sigmoid Function")

plt.plot(
    x,
    sigmoid,
    color="steelblue",
    linewidth=3
)

plt.axhline(
    y=0.5,
    linestyle="--",
    color="red",
    label="Decision Threshold = 0.5"
)

plt.axvline(
    x=0,
    linestyle="--",
    color="black",
    alpha=0.5
)

plt.title("Sigmoid Function",fontweight="bold")
plt.xlabel("Linear Model Output (z)")
plt.ylabel("Probability")

plt.legend()

plt.tight_layout()

plt.show(block=False)

# ------------------------------------------------------------
# FEATURES
#
# X contains everything used to make predictions.
#
# y contains the correct answers.
# ------------------------------------------------------------

X = students[[
    "study_hours",
    "sleep_hours",
    "attendance",
    "assignments"
]]

y = students["passed"]

# ------------------------------------------------------------
# TRAIN / TEST SPLIT
#
# Exactly the same idea as yesterday.
#
# Training data teaches the model.
#
# Testing data evaluates how well it generalizes.
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

print(f"\nTraining Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")

# ------------------------------------------------------------
# FEATURE SCALING
#
# Logistic Regression performs better when features
# are on similar numerical scales.
#
# StandardScaler transforms every feature so that
#
# mean ≈ 0
# std ≈ 1
# ------------------------------------------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)

# ------------------------------------------------------------
# TRAINING THE MODEL
#
# LogisticRegression learns a linear equation
#
# z = w1x1 + w2x2 + ...
#
# and then pushes z through the Sigmoid function
# to produce a probability.
# ------------------------------------------------------------

model = LogisticRegression()

model.fit(

    X_train_scaled,

    y_train

)

# ------------------------------------------------------------
# PREDICTING PROBABILITIES
#
# predict_proba() returns TWO probabilities.
#
# Column 0
# Probability of Class 0
#
# Column 1
# Probability of Class 1
#
# The probabilities always add to 1.
# ------------------------------------------------------------

probabilities = model.predict_proba(X_test_scaled)

predictions = model.predict(X_test_scaled)

print("\nPrediction Results\n")

print(f"{'Student':<10}{'Prob(Fail)':>12}{'Prob(Pass)':>14}{'Prediction':>14}")

print("-"*50)

for i,(fail_prob,pass_prob) in enumerate(probabilities):

    student = students.loc[y_test.index[i],"name"]

    prediction = "Pass" if predictions[i]==1 else "Fail"

    print(
        f"{student:<10}"
        f"{fail_prob:>12.3f}"
        f"{pass_prob:>14.3f}"
        f"{prediction:>14}"
    )

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

print("\n" + "=" * 55)
print(" Classification Evaluation")
print("=" * 55)

# ---- PART 2: the four core classification metrics ----

# ACCURACY
# Accuracy measures the percentage of predictions that
# were completely correct.
#
#                Correct Predictions
# Accuracy = -------------------------------
#                 Total Predictions
#
# WHY THIS MATTERS:
# Accuracy gives an overall idea of model performance.
# However, it can be misleading when one class is much
# more common than the other.

accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy : {accuracy:.4f}")
print(f"           the model correctly classified {accuracy*100:.1f}% of students")

# PRECISION
# Precision answers the question:
#
# "Of all students predicted as PASS,
#  how many actually passed?"
#
#                 True Positives
# Precision = ---------------------------
#              True Positives + False Positives
#
# WHY THIS MATTERS:
# High precision means the model rarely predicts
# PASS incorrectly.

precision = precision_score(y_test, predictions)

print(f"\nPrecision: {precision:.4f}")
print("           higher precision means fewer false pass predictions")

# RECALL
# Recall answers a different question:
#
# "Of all students who actually passed,
#  how many did the model successfully find?"
#
#                 True Positives
# Recall = ------------------------------
#          True Positives + False Negatives
#
# WHY THIS MATTERS:
# High recall means the model rarely misses
# students who should have been classified as PASS.

recall = recall_score(y_test, predictions)

print(f"\nRecall   : {recall:.4f}")
print("           higher recall means fewer missed passing students")

# F1 SCORE
# F1 Score combines Precision and Recall
# into a single metric.
#
#                    2 × Precision × Recall
# F1 = ----------------------------------------------
#            Precision + Recall
#
# WHY THIS MATTERS:
# If either Precision or Recall is poor,
# the F1 Score will also decrease.
#
# F1 is especially useful when we want a
# balance between the two metrics.

f1 = f1_score(y_test, predictions)

print(f"\nF1 Score : {f1:.4f}")
print("           balances both precision and recall")

# CLASSIFICATION REPORT
#
# Instead of calculating each metric manually,
# classification_report() summarizes all major
# evaluation metrics together.
#
# It reports:
#
# Precision
# Recall
# F1 Score
# Support
#
# for every class separately.
#
# WHY THIS MATTERS:
# This is one of the most commonly printed
# summaries when evaluating classification models.

print("\nClassification Report\n")
print(classification_report(
    y_test,
    predictions,
    target_names=["Fail", "Pass"]
))

print("Metric Summary")
print("-" * 35)
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")


from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay
)

# ---- PART 3: Confusion Matrix ----

# A CONFUSION MATRIX tells us exactly which predictions
# were correct and which were incorrect.
#
#                Predicted
#              Fail    Pass
#
# Actual Fail    TN      FP
#
# Actual Pass    FN      TP
#
# TN : True Negative
# Correctly predicted Fail.
#
# TP : True Positive
# Correctly predicted Pass.
#
# FP : False Positive
# Predicted Pass, but actually Fail.
#
# FN : False Negative
# Predicted Fail, but actually Pass.
#
# WHY THIS MATTERS:
#
# Accuracy tells us HOW MANY predictions were correct.
#
# The confusion matrix tells us WHICH predictions
# were correct and WHICH mistakes the model made.

cm = confusion_matrix(y_test, predictions)

print("\nConfusion Matrix")
print(cm)

tn, fp, fn, tp = cm.ravel()

print(f"\nTrue Negatives : {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")
print(f"True Positives : {tp}")

print("\nInterpretation")

if fp == 0:
    print("- The model never incorrectly predicted PASS.")
else:
    print(f"- {fp} student(s) were incorrectly predicted as PASS.")

if fn == 0:
    print("- The model never missed a student who actually passed.")
else:
    print(f"- {fn} student(s) who passed were predicted as FAIL.")

# VISUALIZING THE CONFUSION MATRIX
#
# A heatmap makes it much easier to interpret
# the confusion matrix than raw numbers.
#
# Darker cells represent larger counts.
#
# Ideally:
#
# Most observations should lie on the diagonal.
#
# Top-left  = Correct Fail predictions.
#
# Bottom-right = Correct Pass predictions.
#
# Large values outside the diagonal indicate
# classification mistakes.

fig, ax = plt.subplots(figsize=(6,5), num="Confusion Matrix")

ConfusionMatrixDisplay(

    confusion_matrix=cm,

    display_labels=["Fail", "Pass"]

).plot(

    cmap="Blues",

    colorbar=False,

    ax=ax

)

ax.set_title(
    "Logistic Regression Confusion Matrix",
    fontweight="bold"
)

plt.tight_layout()

plt.show(block=False)

# MISCLASSIFIED STUDENTS
#
# Looking at the confusion matrix tells us
# how many mistakes occurred.
#
# Looking at individual predictions tells us
# WHICH students were misclassified.
#
# WHY THIS MATTERS:
#
# Real machine learning projects almost always
# inspect incorrect predictions to understand
# where the model struggles.

print("\nMisclassified Students")

print(f"{'Student':<10}{'Actual':>10}{'Predicted':>12}")

print("-" * 34)

mistakes = 0

for actual, predicted, index in zip(

    y_test,

    predictions,

    y_test.index

):

    if actual != predicted:

        mistakes += 1

        student = students.loc[index, "name"]

        actual_label = "Pass" if actual else "Fail"

        predicted_label = "Pass" if predicted else "Fail"

        print(

            f"{student:<10}"

            f"{actual_label:>10}"

            f"{predicted_label:>12}"

        )

if mistakes == 0:

    print("None")

print(f"\nTotal Misclassified Students : {mistakes}")

# MODEL PERFORMANCE SUMMARY
#
# Combining the evaluation metrics with the
# confusion matrix gives a much clearer picture
# of model performance.
#
# Metrics such as Accuracy, Precision,
# Recall and F1 Score summarize performance
# numerically.
#
# The Confusion Matrix shows exactly where
# those successes and mistakes occurred.

print("\nEvaluation Summary")
print("-" * 40)
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"Correct Predictions : {tp + tn}")
print(f"Incorrect Predictions : {fp + fn}")

# ---- PART 4: understanding what the model learned ----

# LOGISTIC REGRESSION is still a linear model.
#
# During training, it learns one coefficient for
# every feature.
#
# A POSITIVE coefficient increases the probability
# of belonging to Class 1 (Pass).
#
# A NEGATIVE coefficient decreases the probability
# of belonging to Class 1.
#
# Larger absolute values indicate that the feature
# has a stronger influence on the final prediction.
#
# WHY THIS MATTERS:
#
# Unlike many machine learning models,
# Logistic Regression is highly interpretable.
#
# Instead of simply making predictions,
# we can understand WHY those predictions were made.

coefficients = pd.DataFrame({

    "Feature": X.columns,

    "Coefficient": model.coef_[0]

})

coefficients = coefficients.sort_values(
    by="Coefficient",
    ascending=False
)

print("\nModel Coefficients")
print(coefficients)

print("\nCoefficient Interpretation")

for _, row in coefficients.iterrows():

    feature = row["Feature"]

    value = row["Coefficient"]

    if value > 0:

        print(
            f"{feature:<15}"
            f" Positive ({value:.3f})"
            f" -> increases probability of PASS"
        )

    else:

        print(
            f"{feature:<15}"
            f" Negative ({value:.3f})"
            f" -> decreases probability of PASS"
        )

# VISUALIZING FEATURE IMPORTANCE
#
# A horizontal bar chart makes it much easier
# to compare feature coefficients.
#
# Bars extending to the RIGHT increase the
# probability of PASS.
#
# Bars extending to the LEFT increase the
# probability of FAIL.
#
# Features with larger magnitudes have a
# stronger influence on the prediction.

fig, ax = plt.subplots(
    figsize=(8,5),
    num="Feature Coefficients"
)

ax.barh(

    coefficients["Feature"],

    coefficients["Coefficient"],

    color="steelblue"

)

ax.axvline(

    x=0,

    color="red",

    linestyle="--",

    linewidth=1.5

)

ax.set_title(

    "Feature Coefficients",

    fontweight="bold"

)

ax.set_xlabel("Coefficient Value")

ax.set_ylabel("Feature")

plt.tight_layout()

plt.show(block=False)

# PROBABILITIES VS PREDICTIONS
#
# Logistic Regression predicts probabilities first.
#
# Example:
#
# Student A
# Probability = 0.93
#
# Student B
# Probability = 0.71
#
# Student C
# Probability = 0.18
#
# These probabilities are converted into classes
# using the decision threshold.
#
# By default:
#
# Probability >= 0.50
#
# becomes
#
# PASS
#
# while
#
# Probability < 0.50
#
# becomes
#
# FAIL.
#
# WHY THIS MATTERS:
#
# The model never predicts "Pass" directly.
# It predicts probabilities, and the threshold
# converts those probabilities into classes.

results = pd.DataFrame({

    "Student": students.loc[y_test.index, "name"].values,

    "Actual": np.where(y_test == 1, "Pass", "Fail"),

    "Probability": probabilities[:,1],

    "Prediction": np.where(predictions == 1, "Pass", "Fail")

})

print("\nPrediction Summary")
print(results)

fig, ax = plt.subplots(
    figsize=(8,5),
    num="Predicted Probabilities"
)

ax.bar(

    results["Student"],

    results["Probability"],

    color="mediumseagreen"

)

ax.axhline(

    y=0.5,

    color="red",

    linestyle="--",

    linewidth=1.5,

    label="Decision Threshold"

)

ax.set_ylim(0,1)

ax.set_ylabel("Probability of Passing")

ax.set_title(

    "Predicted Pass Probability",

    fontweight="bold"

)

ax.legend()

plt.tight_layout()

plt.show(block=False)



# ---- PART 5: predicting completely new students ----

# So far we evaluated the model using the testing set.
#
# However, the real purpose of Machine Learning is to make
# predictions on NEW data that the model has never seen before.
#
# These examples simulate brand-new students.
#
# WHY THIS MATTERS:
#
# If the model performs well only on the training data,
# it has simply memorized the dataset.
#
# A useful model should generalize and make reasonable
# predictions for unseen observations.

new_students = pd.DataFrame({

    "study_hours":[2,5,8],

    "sleep_hours":[5,7,8],

    "attendance":[65,85,97],

    "assignments":[5,8,10]

})

print("\nNew Students")
print(new_students)

# We MUST use the SAME scaler that was fitted on the
# training data.
#
# Never fit another scaler on new data because that
# would change the feature distributions the model
# learned during training.

new_students_scaled = scaler.transform(new_students)

# predict_proba() gives probabilities.
#
# predict() converts those probabilities into
# PASS or FAIL using the default threshold of 0.5.

new_probabilities = model.predict_proba(new_students_scaled)

new_predictions = model.predict(new_students_scaled)

print("\nPredictions for New Students")

print(f"{'Student':<10}{'Pass Probability':>20}{'Prediction':>15}")

print("-"*48)

for i in range(len(new_students)):

    probability = new_probabilities[i][1]

    prediction = "Pass" if new_predictions[i] else "Fail"

    print(

        f"Student {i+1:<2}"

        f"{probability:>16.3f}"

        f"{prediction:>15}"

    )

# VISUALIZING THE NEW PREDICTIONS
#
# Taller bars indicate higher confidence that
# the student will PASS.
#
# Bars below the red dashed line are classified
# as FAIL.
#
# WHY THIS MATTERS:
#
# This visualization makes it much easier to see
# both the prediction AND the confidence behind it.

fig, ax = plt.subplots(

    figsize=(8,5),

    num="Predictions for New Students"

)

labels = [f"Student {i}" for i in range(1,4)]

ax.bar(

    labels,

    new_probabilities[:,1],

    color="mediumseagreen"

)

ax.axhline(

    y=0.5,

    color="red",

    linestyle="--",

    linewidth=1.5,

    label="Decision Threshold"

)

for i, probability in enumerate(new_probabilities[:,1]):

    ax.text(

        i,

        probability + 0.03,

        f"{probability:.2f}",

        ha="center",

        fontsize=9

    )

ax.set_ylim(0,1.05)

ax.set_ylabel("Probability of Passing")

ax.set_title(

    "Predictions for Unseen Students",

    fontweight="bold"

)

ax.legend()

plt.tight_layout()

plt.savefig(

    "logistic_regression.png",

    dpi=150,

    bbox_inches="tight"

)

plt.show(block=False)

# WHAT DID WE LEARN TODAY?
#
# Logistic Regression is one of the most widely used
# classification algorithms.
#
# Unlike Linear Regression, it predicts probabilities
# instead of continuous values.
#
# Those probabilities are converted into classes using
# the Sigmoid Function and a decision threshold.
#
# We also learned how to evaluate a classifier using:
#
# Accuracy
# Precision
# Recall
# F1 Score
# Confusion Matrix
#
# Finally, we predicted completely unseen students
# and interpreted the confidence of those predictions.

print("\n" + "="*55)
print(" Day 52 Summary ")
print("="*55)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nModel Successfully Trained.")

print("Predictions Generated.")

print("Evaluation Complete.")

print("Saved Figure : logistic_regression.png")

plt.ioff()
plt.show()


# ---- BONUS: changing the decision threshold ----

# Earlier we learned that Logistic Regression predicts
# probabilities between 0 and 1.
#
# By default, sklearn converts probabilities into classes
# using a threshold of 0.50.
#
# Probability >= 0.50
# -> Pass
#
# Probability < 0.50
# -> Fail
#
# However, this threshold is NOT fixed.
#
# We can choose another threshold depending on the problem.
#
# WHY THIS MATTERS:
#
# Lowering the threshold predicts PASS more often,
# increasing Recall but decreasing Precision.
#
# Raising the threshold predicts PASS less often,
# increasing Precision but decreasing Recall.

threshold = 0.70

custom_predictions = (probabilities[:, 1] >= threshold).astype(int)

print(f"\nDecision Threshold = {threshold}")

print(f"\n{'Student':<10}{'Probability':>15}{'Prediction':>15}")

print("-" * 40)

for i, probability in enumerate(probabilities[:, 1]):

    student = students.loc[y_test.index[i], "name"]

    prediction = "Pass" if custom_predictions[i] else "Fail"

    print(
        f"{student:<10}"
        f"{probability:>15.3f}"
        f"{prediction:>15}"
    )

fig, ax = plt.subplots(figsize=(8,5), num="Decision Threshold")

student_names = students.loc[y_test.index, "name"]

ax.bar(student_names, probabilities[:,1], color="steelblue")

ax.axhline(
    y=threshold,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Threshold = {threshold}"
)

ax.set_ylim(0,1)

ax.set_title(
    "Changing the Decision Threshold",
    fontweight="bold"
)

ax.set_ylabel("Probability of Passing")

ax.legend()

plt.tight_layout()

plt.show(block=False)



# ---- PART 7: Putting Everything Together ----

# Machine Learning is not just about training a model.
#
# A complete workflow usually follows these steps:
#
# 1. Collect data.
# 2. Prepare the features.
# 3. Split the dataset.
# 4. Scale numerical features.
# 5. Train the model.
# 6. Evaluate the model.
# 7. Predict unseen data.
# 8. Interpret the results.
#
# WHY THIS MATTERS:
#
# Most real-world machine learning projects follow
# exactly this pipeline regardless of the algorithm.
#
# Understanding the workflow is often more important
# than memorizing the syntax.

print("\n" + "=" * 60)
print(" COMPLETE LOGISTIC REGRESSION WORKFLOW ")
print("=" * 60)

print("\n1. Dataset Created")
print(f"   Total Students : {len(students)}")

print("\n2. Features Selected")
print(f"   {list(X.columns)}")

print("\n3. Dataset Split")
print(f"   Training : {len(X_train)}")
print(f"   Testing  : {len(X_test)}")

print("\n4. Features Standardized")
print("   Mean ≈ 0")
print("   Standard Deviation ≈ 1")

print("\n5. Logistic Regression Model Trained")

print("\n6. Model Evaluated")
print(f"   Accuracy : {accuracy:.3f}")
print(f"   Precision: {precision:.3f}")
print(f"   Recall   : {recall:.3f}")
print(f"   F1 Score : {f1:.3f}")

print("\n7. Predictions Generated")
print(f"   Test Predictions : {len(predictions)}")
print(f"   New Students     : {len(new_predictions)}")

print("\n8. Figure Saved")
print("   logistic_regression.png")

print("\nWorkflow Complete.")

# FINAL TAKEAWAYS
#
# Linear Regression predicts continuous values.
#
# Logistic Regression predicts probabilities.
#
# Those probabilities are converted into classes
# using the Sigmoid Function and a decision threshold.
#
# Classification models are evaluated using:
#
# Accuracy
# Precision
# Recall
# F1 Score
# Confusion Matrix
#
# Logistic Regression is one of the most widely used
# classification algorithms because it is both
# accurate and highly interpretable.

print("\n" + "=" * 60)
print(" KEY TAKEAWAYS ")
print("=" * 60)

print("""
• Binary Classification predicts classes instead of numbers.

• Logistic Regression outputs probabilities between 0 and 1.

• The Sigmoid Function converts any real value into a probability.

• A threshold (usually 0.50) converts probabilities into classes.

• Accuracy measures overall correctness.

• Precision measures how reliable positive predictions are.

• Recall measures how many actual positives were found.

• F1 Score balances Precision and Recall.

• The Confusion Matrix explains where predictions were correct
  and where mistakes occurred.

• Model coefficients show which features influence predictions
  the most.
""")

print("=" * 60)
print(" End of Day 52 ")
print("=" * 60)
