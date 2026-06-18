import numpy as np
#slicing and indexing, selecting a range of data points from a certain index in numpy.
#   setup: a sample dataset, students x subjects  
scores = np.array([
    [85, 92, 78, 88],   # student 0
    [90, 88, 95, 79],   # student 1
    [70, 75, 80, 92],   # student 2
    [88, 91, 84, 85],   # student 3
    [95, 89, 91, 97],   # student 4
])
print(f"Full dataset:\n{scores}\n")

#   PART 1: selecting a single row  
# row index, all columns
print(f"Student 0's scores : {scores[0]}")
print(f"Student 2's scores : {scores[2]}")

#   PART 2: selecting a single column  
# the : means "all rows", then pick the column index
print(f"\nAll Math scores (col 0)    : {scores[:, 0]}")
print(f"All Science scores (col 1) : {scores[:, 1]}")

#   PART 3: selecting a single cell  
# [row, col] — direct access, no nested indexing needed
print(f"\nStudent 1's Science score : {scores[1, 1]}")
print(f"Student 4's English score : {scores[4, 2]}")

#   PART 4: slicing ranges — rows AND columns together  
# [start:end, start:end] — end is exclusive, just like regular slicing
print(f"\nFirst 3 students, first 2 subjects:\n{scores[0:3, 0:2]}")

# every other row
print(f"\nEvery other student:\n{scores[::2]}")

# last 2 students, last 2 subjects
print(f"\nLast 2 students, last 2 subjects:\n{scores[-2:, -2:]}")

#   PART 5: modifying a slice  
# slices are VIEWS, not copies — editing one changes the original array
scores_copy = scores.copy()   # use .copy() if you don't want this side effect
scores_copy[0, :] = [100, 100, 100, 100]   # give student 0 perfect scores
print(f"\nAfter modifying student 0:\n{scores_copy}")

#   PART 6: practical pattern — extract a feature column for analysis  
# this is exactly how you'd pull a single column to analyze in real DS work
math_scores = scores[:, 0]
print(f"\nMath scores across all students : {math_scores}")
print(f"Highest Math score               : {math_scores.max()}")
print(f"Student index with highest Math  : {math_scores.argmax()}")   # which student?