import numpy as np

# ---- PART 1: inspecting shape ----
# .shape tells you the dimensions — always check this first when debugging
arr = np.arange(1, 13)   # 1D array: [1, 2, 3, ..., 12]
print(f"Original array : {arr}")
print(f"Shape          : {arr.shape}")    # (12,) — 12 elements, 1D
print(f"Ndim           : {arr.ndim}")     # 1

# ---- PART 2: reshape into 2D ----
# reshape(rows, cols) — total elements must match (4*3 = 12, fits)
matrix_4x3 = arr.reshape(4, 3)
print(f"\nReshaped to (4,3):\n{matrix_4x3}")
print(f"Shape : {matrix_4x3.shape}")
print(f"Ndim  : {matrix_4x3.ndim}")

# try a different shape — same data, different layout
matrix_3x4 = arr.reshape(3, 4)
print(f"\nReshaped to (3,4):\n{matrix_3x4}")

matrix_2x6 = arr.reshape(2, 6)
print(f"\nReshaped to (2,6):\n{matrix_2x6}")

# ---- PART 3: flatten back to 1D ----
# .flatten() or .reshape(-1) collapses any shape back to a single row
flat_again = matrix_4x3.flatten()
print(f"\nFlattened back  : {flat_again}")

# ---- PART 4: the magic of -1 in reshape ----
# -1 tells NumPy "figure out this dimension yourself"
# useful when you know one dimension but not the other
auto_reshape = arr.reshape(-1, 4)   # "give me 4 columns, calculate rows"
print(f"\nReshape(-1, 4):\n{auto_reshape}")
print(f"Shape          : {auto_reshape.shape}")   # NumPy figures out (3, 4)

# ---- PART 5: reshape will error if sizes don't match ----
# this is intentional — catching this early matters in real pipelines
try:
    bad_reshape = arr.reshape(5, 5)   # 12 elements can't fit into 25 slots
except ValueError as e:
    print(f"\n❌ Reshape failed: {e}")

# ---- PART 6: 3D reshape — going beyond tables ----
# common in image data: (height, width, channels)
cube = arr.reshape(2, 2, 3)
print(f"\nReshaped to 3D (2,2,3):\n{cube}")
print(f"Shape : {cube.shape}")
print(f"Ndim  : {cube.ndim}")   # 3 — this is what an RGB image array looks like