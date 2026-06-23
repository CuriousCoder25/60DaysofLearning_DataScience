import numpy as np
import matplotlib.pyplot as plt

# seed makes randomness repeatable
# same seed = same results every run
np.random.seed(42)

# randint upper bound is exclusive
# (1,7) means 1 to 6
rolls = np.random.randint(1, 7, size=10)

print("sample rolls")
print(rolls)

# random floats between 0 and 1
floats = np.random.rand(5)

print("\nfloats")
print(floats)

# normal distribution
# values mostly near 0, extremes are rare
normal = np.random.randn(10)

print("\nnormal distribution")
print(normal)


# random selection from list
langs = np.array(["python", "java", "cpp", "js"])

picked = np.random.choice(langs, size=5)

print("\nrandom selection")
print(picked)


# shuffle modifies array in place
arr = np.array([10, 20, 30, 40, 50])

print("\nbefore shuffle")
print(arr)

np.random.shuffle(arr)

print("after shuffle")
print(arr)


# dice simulation
# checking if outcomes are evenly distributed
dice = np.random.randint(1, 7, size=10000)

print("\nfirst 20 rolls")
print(dice[:20])


# frequency count
unique, counts = np.unique(dice, return_counts=True)

print("\nfrequency")

for u, c in zip(unique, counts):
    print(u, c)


# histogram for visual check
plt.hist(
    dice,
    bins=np.arange(1, 8) - 0.5,
    edgecolor="black"
)

plt.xticks(range(1, 7))
plt.title("dice simulation")
plt.show()


# two dice simulation
# sum is not uniform, 7 appears most often
d1 = np.random.randint(1, 7, 10000)
d2 = np.random.randint(1, 7, 10000)

total = d1 + d2

plt.hist(
    total,
    bins=np.arange(2, 14) - 0.5,
    edgecolor="black"
)

plt.title("two dice sum")
plt.show()