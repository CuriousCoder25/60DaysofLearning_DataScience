import numpy as np

# ---- setup: same student scores dataset ----
scores = np.array([
    [85, 92, 78, 88],
    [90, 88, 95, 79],
    [70, 75, 80, 92],
    [88, 91, 84, 85],
    [95, 89, 91, 97],
])
print(f"Full dataset:\n{scores}\n")

# ---- PART 1: the boolean mask itself ----
# comparing an array to a value returns an array of True/False
# this is the mask — same shape as original, but boolean
mask = scores > 85
print(f"Mask (scores > 85):\n{mask}\n")

# ---- PART 2: applying the mask to filter values ----
# scores[mask] pulls out only the True positions — flattened result
high_scores = scores[mask]
print(f"All scores above 85 : {high_scores}")

# same thing in one line — this is the real-world usage pattern
print(f"Same, inline         : {scores[scores > 85]}")

# ---- PART 3: combining conditions ----
# use & for AND, | for OR — NOT the Python 'and'/'or' keywords
# each condition must be wrapped in parentheses
between = scores[(scores > 75) & (scores < 90)]
print(f"\nScores between 75 and 90 : {between}")

extreme = scores[(scores < 75) | (scores > 95)]
print(f"Scores below 75 or above 95 : {extreme}")

# ---- PART 4: masking on a single column ----
# pull Math scores (col 0), then find which students scored above average
math_scores = scores[:, 0]
avg_math = math_scores.mean()
print(f"\nMath scores      : {math_scores}")
print(f"Average Math     : {avg_math:.1f}")
print(f"Above-average    : {math_scores[math_scores > avg_math]}")

# ---- PART 5: using the mask to find WHICH students, not just values ----
# np.where returns the indices where the condition is True
above_avg_indices = np.where(math_scores > avg_math)[0]
print(f"\nStudent indices scoring above average Math : {above_avg_indices}")

# ---- PART 6: practical use — flag failing students across ALL subjects ----
# a student "passes" only if every single score is >= 80
passing_mask = np.all(scores >= 80, axis=1)   # axis=1 checks across each row
print(f"\nPassing mask (all subjects >= 80) : {passing_mask}")
print(f"Students who pass everything       : {np.where(passing_mask)[0]}")
print(f"Their full score rows:\n{scores[passing_mask]}")