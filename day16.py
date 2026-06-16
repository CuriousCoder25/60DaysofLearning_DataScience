#beggining numpy library practice
#make an venv and install  numpy:  pip install numpy
import numpy as np

# ---- PART 1: Python list vs NumPy array ----
# the core problem with plain Python lists for data work:
# looping over them is slow — they store pointers, not raw values
py_list = [1, 2, 3, 4, 5]
np_array = np.array([1, 2, 3, 4, 5])

print(f"Python list  : {py_list}")
print(f"NumPy array  : {np_array}")
print(f"Type         : {type(np_array)}")
print(f"dtype        : {np_array.dtype}")   # int32/int64 — stored as actual numbers

# ---- PART 2: why NumPy is faster — no loops needed ----
# with a Python list you'd loop to square every element
# NumPy does it on the whole array at once — C speed under the hood
squared_list  = [x**2 for x in py_list]       # Python way — loop
squared_numpy = np_array ** 2                  # NumPy way — vectorized

print(f"\nSquared (list) : {squared_list}")
print(f"Squared (numpy): {squared_numpy}")

# ---- PART 3: creating arrays different ways ----
zeros   = np.zeros(5)             # all zeros — useful for placeholders
ones    = np.ones(5)              # all ones
range_a = np.arange(0, 10, 2)    # like Python range() but returns array
linspace = np.linspace(0, 1, 5)  # 5 evenly spaced values between 0 and 1

print(f"\nnp.zeros    : {zeros}")
print(f"np.ones     : {ones}")
print(f"np.arange   : {range_a}")
print(f"np.linspace : {linspace}")

# ---- PART 4: 2D array — the core DS data structure ----
# think of this as a table: rows = records, columns = features
scores = np.array([
    [85, 92, 78],   # student 1 — math, science, english
    [90, 88, 95],   # student 2
    [70, 75, 80],   # student 3
    [88, 91, 84],   # student 4
])

print(f"\n2D scores array:\n{scores}")
print(f"\nShape  : {scores.shape}")    # (4, 3) — 4 rows, 3 columns
print(f"Dims   : {scores.ndim}")      # 2 — it's a 2D array
print(f"Size   : {scores.size}")      # 12 — total elements
print(f"dtype  : {scores.dtype}")     # int64

# ---- PART 5: basic operations on the 2D array ----
print(f"\nMean score per student : {scores.mean(axis=1)}")  # row-wise
print(f"Mean score per subject : {scores.mean(axis=0)}")   # col-wise
print(f"Highest score overall  : {scores.max()}")
print(f"Lowest score overall   : {scores.min()}")