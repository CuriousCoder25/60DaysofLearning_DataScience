import numpy as np

#Dot product intuition: multipying matching elements, then add them all up.
# [2, 3] . [4, 5]  =  (2*4) + (3*5)  =  8 + 15  =  23
# Thats the whole logic and below is implementation.

a = np.array([2, 3])
b = np.array([4, 5])
print(f"Dot product of {a} and {b} : {np.dot(a, b)}") 

# PART 1: the weighted score problem 
# This is THE real-world reason dot products matter:
# you have raw scores, and you have weights for each subject.
# Dot product = multiply each score by its weight, then sum it all in ONE operation instead of a manual loop with running totals.

scores = np.array([85, 92, 78, 88])              # Math, Science, English, History
weights = np.array([0.4, 0.3, 0.2, 0.1])         # Math matters most, History least

final_score = np.dot(scores, weights)
print(f"\nScores  : {scores}")
print(f"Weights : {weights}")
print(f"Weighted final score : {final_score:.2f}")

# manual version, just to prove the dot product is doing exactly this:
manual = (85*0.4) + (92*0.3) + (78*0.2) + (88*0.1)
print(f"Manual calculation   : {manual:.2f}  <- matches!!")


# PART 2: matrix @ matrix -- multiple students at once 
# REMEMBER THIS RULE: for A @ B to work,
# A's number of COLUMNS must equal B's number of ROWS.
# Shape (5,4) @ (4,) works because 4 == 4. That's the whole rule.

# KEY TAKEAWAY: matrix multiplication is JUST the dot product
# (multiply pairs, then add) applied row-by-row across an entire
# table at once. Nothing new is happening here conceptually: it's the same operation from Part 1, just repeated automatically.


all_scores = np.array([
    [85, 92, 78, 88],
    [90, 88, 95, 79],
    [70, 75, 80, 92],
    [88, 91, 84, 85],
    [95, 89, 91, 97],
])

# this computes the weighted score for ALL 5 students in one line ,
# no loop needed, because @ applies the dot product row by row automatically
weighted_scores = all_scores @ weights
print(f"\nAll students' weighted scores : {weighted_scores}")

#  PART 3: np.dot vs @ , they're the same thing for this case 
# @ is just cleaner syntax, introduced specifically for matrix multiplication
same_result = np.dot(all_scores, weights)
print(f"Using np.dot (same result)    : {same_result}")

#  PART 4: matrix @ matrix (not just matrix @ vector) 
# Two weighting SCHEMES at once , e.g. "STEM-focused" vs "Balanced"
#
# WHY .T IS HERE , the part that trips people up the most:
# .T (transpose) flips rows and columns. It has NOTHING to do with
# the math itself , it's purely here to make the SHAPES compatible
# so @ is allowed to run. If you ever get a shape error on @,
# check whether a .T is missing before debugging anything else.
weight_schemes = np.array([
    [0.4, 0.3, 0.2, 0.1],   # STEM-focused: favors Math heavily
    [0.25, 0.25, 0.25, 0.25],  # Balanced: equal weight everywhere
]).T

# shape check: (5,4) @ (4,2) -> result is (5,2): 5 students, 2 scoring schemes
results = all_scores @ weight_schemes
print(f"\nShape of result : {results.shape}")
print(f"STEM-focused vs Balanced scores per student:\n{results}")