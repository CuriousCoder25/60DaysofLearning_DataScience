import numpy as np
from PIL import Image

# Load any image you have , a photo, a screenshot, anything
img = Image.open("photo.jpg")
img_array = np.array(img)

# IMAGES ARE JUST 3D ARRAYS , this connects directly back to
# Day 17 where you reshaped arrays into (height, width, channels).
# Every pixel has 3 numbers: Red, Green, Blue (0-255 each).
print(f"Image shape: {img_array.shape}")   # e.g. (600, 800, 3)
print(f"Data type  : {img_array.dtype}")   # usually uint8

# THE GRAYSCALE FORMULA , not a simple average of R, G, B.
# Human eyes are more sensitive to green, less to blue.
# These specific weights (0.299, 0.587, 0.114) come from how
# the eye perceives brightness , this is the EXACT same
# "weighted sum" idea from Day 22's linear algebra lesson,
# just applied to pixels instead of test scores.
weights = np.array([0.299, 0.587, 0.114])

# @ multiplies each pixel's RGB values by the weights and sums them ,
# same dot product operation from Day 22, just on millions of pixels at once
grayscale = img_array[:, :, :3] @ weights

# Convert back to whole numbers (0-255) for a valid image
grayscale = grayscale.astype(np.uint8)

print(f"\nGrayscale shape: {grayscale.shape}")   # now 2D, no color channel needed

# Save the result
gray_img = Image.fromarray(grayscale)
gray_img.save("grayscale_output.jpg")
print("Saved grayscale_output.jpg")

# BONUS , compare brightness stats before and after
print(f"\nOriginal avg brightness (per channel): {img_array[:,:,:3].mean(axis=(0,1))}")
print(f"Grayscale avg brightness              : {grayscale.mean():.2f}")