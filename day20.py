import numpy as np

scores = np.array([
    [85, 92, 78, 88],
    [90, 88, 95, 79],
    [70, 75, 80, 92],
    [88, 91, 84, 85],
    [95, 89, 91, 97],
])
print(f"Original scores:\n{scores}\n")

# BROADCASTING = NumPy automatically "stretches" a smaller array
# to match a bigger one, so the operation applies everywhere at once.
# This is why NumPy never needs a for-loop to do +5 to every value.
curved = scores + 5
print(f"Curved (+5 everywhere):\n{curved}\n")

scaled = scores * 1.1
print(f"Scaled (x1.1):\n{scaled}\n")

# Here's broadcasting actually proving its worth:
# subject_weights has only 4 numbers, but scores has 20.
# NumPy lines up the 4 weights against EACH ROW's 4 columns,
# repeating them 5 times (once per student) without me writing that loop.
subject_weights = np.array([1.2, 1.0, 0.8, 1.0])
print(f"Subject weights : {subject_weights}")

weighted = scores * subject_weights
print(f"\nWeighted scores:\n{weighted}\n")

# THE BROADCASTING RULE (memorize this, it's the whole concept):
# Compare shapes from the RIGHT side.
#   scores : (5, 4)
#   weights: (   4,)  <- matches the last dimension (4), so it's allowed
# If the last dimension doesn't match AND isn't 1, NumPy throws an error.
try:
    bad = scores * np.array([1, 2, 3])   # 3 doesn't match 4 -> fails on purpose
except ValueError as e:
    print(f"❎ Broadcasting failed: {e}\n")

# WHY NORMALIZE: if I feed raw scores into an ML model later,
# a value of 95 isn't "more important" than 0.95 — but the model
# might think so just because the number is bigger. Squashing
# everything into the same 0–1 range fixes that distortion.
min_val = scores.min()
max_val = scores.max()
normalized = (scores - min_val) / (max_val - min_val)
print(f"Normalized (0-1 range):\n{np.round(normalized, 2)}\n")

# WHY PER-COLUMN, NOT GLOBAL: each subject has its own difficulty curve.
# Normalizing the WHOLE table at once mixes Math's range with English's
# range — that's misleading. Normalizing PER COLUMN treats each subject
# fairly, on its own scale. This is what real preprocessing actually does.
col_min = scores.min(axis=0)
col_max = scores.max(axis=0)
col_normalized = (scores - col_min) / (col_max - col_min)

print(f"Per-subject min : {col_min}")
print(f"Per-subject max : {col_max}")
print(f"\nPer-column normalized:\n{np.round(col_normalized, 2)}")