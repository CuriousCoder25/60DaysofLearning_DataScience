import numpy as np

scores = np.array([
    [85, 92, 78, 88],
    [90, 88, 95, 79],
    [70, 75, 80, 92],
    [88, 91, 84, 85],
    [95, 89, 91, 97],
])
print(f"Scores (rows=students, cols=subjects):\n{scores}\n")

# Whole-array aggregation collapses EVERYTHING into one number.
# Use this when you just need "the big picture," not a breakdown.
print(f"Total sum     : {scores.sum()}")
print(f"Overall mean  : {scores.mean():.2f}")
print(f"Overall std   : {scores.std():.2f}")

# THE TRICK TO REMEMBER axis=0 vs axis=1:
# axis=0 means "walk DOWN the rows" -> result is per COLUMN (per subject)
# axis=1 means "walk ACROSS the columns" -> result is per ROW (per student)
# Mnemonic: the axis number tells you which direction you're COLLAPSING,
# not which one survives. axis=0 collapses rows, so columns survive.
print(f"\n--- axis=0: per subject (collapses students) ---")
print(f"Mean per subject : {scores.mean(axis=0)}")

print(f"\n--- axis=1: per student (collapses subjects) ---")
print(f"Mean per student : {scores.mean(axis=1)}")

# Real use case: average per student = their report card grade.
# Average per subject = how hard/easy that subject was for the whole class.
# Same numbers, totally different meaning depending on which axis you pick.
student_avg = scores.mean(axis=1)
subject_avg = scores.mean(axis=0)

print(f"\n--- Report Card ---")
subjects = ["Math", "Science", "English", "History"]
for i, avg in enumerate(student_avg):
    print(f"Student {i} average : {avg:.1f}")
print()
for subj, avg in zip(subjects, subject_avg):
    print(f"{subj:<10} class average : {avg:.1f}")

# STD INTUITION: it measures how SPREAD OUT the numbers are from the mean.
# Low std = scores are clustered close together = consistent performance.
# High std = scores are scattered = some subjects much stronger/weaker than others.
# Two students can have the SAME average but very different std —
# that's the whole point of checking std separately from mean.
student_std = scores.std(axis=1)
print(f"\n--- Consistency Check (std per student) ---")
for i, std in enumerate(student_std):
    tag = "Consistent" if std < 6 else "Inconsistent"
    print(f"Student {i} : std={std:.2f} -> {tag}")