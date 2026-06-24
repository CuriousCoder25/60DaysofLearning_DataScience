import numpy as np

# setup: two separate datasets to combine 
# imagine these came from two different CSV files you loaded separately
midterm_scores = np.array([
    [85, 92, 78],
    [90, 88, 95],
    [70, 75, 80],
])

final_scores = np.array([
    [88, 91, 80],
    [92, 85, 97],
    [75, 78, 85],
])
print(f"Midterm scores:\n{midterm_scores}\n")
print(f"Final scores:\n{final_scores}\n")

# hstack joins arrays SIDE BY SIDE, adding more COLUMNS.
# It only works if both arrays have the same number of ROWS,
# here both have 3 rows (3 students), so they line up cleanly.
# WHY THIS MATTERS: this is how you'd merge "midterm.csv" and
# "final.csv" for the SAME students into one wider table.
combined_subjects = np.hstack((midterm_scores, final_scores))
print(f"hstack result (3 students, now 6 score columns):\n{combined_subjects}")
print(f"Shape : {combined_subjects.shape}\n")

# vstack joins arrays ON TOP of each other, adding more ROWS.
# It only works if both arrays have the same number of COLUMNS.
# WHY THIS MATTERS: this is how you'd add NEW students to an
# existing dataset without touching the existing rows at all.
new_students = np.array([
    [60, 65, 70],
    [82, 84, 88],
])
all_students = np.vstack((midterm_scores, new_students))
print(f"vstack result (now 5 students, same 3 subjects):\n{all_students}")
print(f"Shape : {all_students.shape}\n")

# np.concatenate is the general-purpose tool behind both of the above 
# axis=1 behaves like hstack (sideways), axis=0 behaves like vstack (stacked).
# WHY THIS MATTERS: if you ever forget which stack function does what,
# fall back to concatenate and just pick the axis , same result, no guessing.
concat_side = np.concatenate((midterm_scores, final_scores), axis=1)
concat_stack = np.concatenate((midterm_scores, new_students), axis=0)

print(f"concatenate axis=1 (same as hstack)? {np.array_equal(concat_side, combined_subjects)}")
print(f"concatenate axis=0 (same as vstack)? {np.array_equal(concat_stack, all_students)}")

# Stacking monthly attendance arrays into one table ,
# jan/feb/mar each have 3 values (one per student), stacked as rows
# means the result shape becomes (3 months, 3 students).
# WHY THIS MATTERS: this is EXACTLY what pd.concat() will do for you
# in Pandas (Phase 3, Day 36) when merging monthly CSV files into
# one yearly dataset , you're learning the underlying logic now,
# before the library hides it behind a friendlier function name.
jan = np.array([22, 20, 19])
feb = np.array([18, 21, 20])
mar = np.array([20, 19, 22])

quarterly = np.vstack((jan, feb, mar))
print(f"\nQuarterly attendance (rows=months, cols=students):\n{quarterly}")
print(f"Total attendance per student (sum down columns) : {quarterly.sum(axis=0)}")