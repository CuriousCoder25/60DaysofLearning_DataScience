import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.ion()
sns.set_theme(style="whitegrid", palette="muted")

scores = np.array([88, 92, 75, 95, 81, 65, 97, 80, 90, 70])

print("=" * 45)
print("  Stats Foundations : Day 47")
print("=" * 45)

# ---- PART 1: manual calculations first ----
# WHY WE DO THIS MANUALLY FIRST: NumPy functions like .mean() and
# .std() are black boxes. computing them by hand once locks in WHAT
# they actually calculate, so we're not just calling magic functions.

# MEAN: sum of all values divided by count.
# represents the "center of gravity" of the data.
mean_manual = sum(scores) / len(scores)
mean_numpy  = np.mean(scores)
print(f"\nMean (manual) : {mean_manual:.2f}")
print(f"Mean (numpy)  : {mean_numpy:.2f}  <- same result")

# MEDIAN: the middle value when sorted.
# unlike mean, median is NOT pulled by extreme outliers.
# if one student scored 5 instead of 65, mean drops dramatically
# but median barely moves : that's why median is more "robust".
sorted_scores = np.sort(scores)
n = len(sorted_scores)
if n % 2 == 0:
    median_manual = (sorted_scores[n//2 - 1] + sorted_scores[n//2]) / 2
else:
    median_manual = sorted_scores[n//2]

median_numpy = np.median(scores)
print(f"\nMedian (manual) : {median_manual:.2f}")
print(f"Median (numpy)  : {median_numpy:.2f}  <- same result")

# VARIANCE: average of squared distances from the mean.
# squaring does two things: removes negatives, and penalizes
# values far from the mean MORE than values close to it.
# ddof=1 means "divide by n-1 instead of n" : this is Bessel's
# correction, used when our data is a SAMPLE not the full population.
# WHY THIS MATTERS: almost all real datasets are samples, not
# the full population, so ddof=1 is almost always the right choice.
variance_manual = sum((x - mean_manual) ** 2 for x in scores) / (len(scores) - 1)
variance_numpy  = np.var(scores, ddof=1)
print(f"\nVariance (manual) : {variance_manual:.2f}")
print(f"Variance (numpy)  : {variance_numpy:.2f}  <- same result")

# STANDARD DEVIATION: square root of variance.
# brings the unit back to the original scale (scores, not scores²)
# so it's directly interpretable: "scores typically deviate by
# ±X points from the mean."
std_manual = variance_manual ** 0.5
std_numpy  = np.std(scores, ddof=1)
print(f"\nStd Dev (manual) : {std_manual:.2f}")
print(f"Std Dev (numpy)  : {std_numpy:.2f}  <- same result")

# ---- PART 2: distributions ----
# a distribution describes how values are spread across a range.
# NORMAL DISTRIBUTION (bell curve): most values cluster near the
# mean, fewer values as we move further away. symmetric shape.
# WHY THIS MATTERS: many ML algorithms ASSUME data is normally
# distributed. if it isn't, results can be unreliable.

np.random.seed(42)
normal_data  = np.random.normal(loc=80, scale=10, size=1000)  # mean=80, std=10
skewed_data  = np.random.exponential(scale=15, size=1000)      # right-skewed

plt.figure(figsize=(12, 4), num="Distributions")

plt.subplot(1, 2, 1)
sns.histplot(normal_data, kde=True, color="steelblue", bins=30)
plt.axvline(np.mean(normal_data), color="red", linestyle="--",
    label=f"Mean ({np.mean(normal_data):.1f})")
plt.axvline(np.median(normal_data), color="orange", linestyle="--",
    label=f"Median ({np.median(normal_data):.1f})")
plt.title("Normal Distribution\n(mean ≈ median)", fontweight="bold")
plt.legend(fontsize=8)

plt.subplot(1, 2, 2)
sns.histplot(skewed_data, kde=True, color="coral", bins=30)
plt.axvline(np.mean(skewed_data), color="red", linestyle="--",
    label=f"Mean ({np.mean(skewed_data):.1f})")
plt.axvline(np.median(skewed_data), color="orange", linestyle="--",
    label=f"Median ({np.median(skewed_data):.1f})")
plt.title("Skewed Distribution\n(mean pulled by outliers)", fontweight="bold")
plt.legend(fontsize=8)

plt.suptitle("Normal vs Skewed : why median is more robust",
    fontsize=12, fontweight="bold")
plt.tight_layout()
plt.show(block=False)

# ---- PART 3: correlation revisited ----
# we computed .corr() in Day 44 using Pandas. here we compute
# the Pearson correlation coefficient MANUALLY to understand
# what the formula is actually doing under the hood.
#
# PEARSON FORMULA: r = Σ((x - x̄)(y - ȳ)) / (n-1) * std_x * std_y
# it measures how much x and y move TOGETHER relative to their
# individual spreads. result between -1 and 1.
study_hours = np.array([4, 6, 3, 7, 5, 2, 8, 4, 6, 3])

# manual Pearson correlation
x_dev = study_hours - np.mean(study_hours)   # deviation from mean
y_dev = scores - np.mean(scores)

r_manual = np.sum(x_dev * y_dev) / ((len(scores) - 1) *
    np.std(study_hours, ddof=1) * np.std(scores, ddof=1))
r_numpy  = np.corrcoef(study_hours, scores)[0, 1]

print(f"\nPearson r (manual) : {r_manual:.4f}")
print(f"Pearson r (numpy)  : {r_numpy:.4f}  <- same result")
print(f"\nInterpretation: {'strong' if abs(r_manual) > 0.7 else 'moderate' if abs(r_manual) > 0.4 else 'weak'} "
      f"{'positive' if r_manual > 0 else 'negative'} correlation")

# ---- PART 4: summary stats side by side ----
print(f"\n{'='*45}")
print(f"  Full Summary")
print(f"{'='*45}")
print(f"  Mean     : {mean_numpy:.2f}")
print(f"  Median   : {median_numpy:.2f}")
print(f"  Variance : {variance_numpy:.2f}")
print(f"  Std Dev  : {std_numpy:.2f}")
print(f"  Min      : {scores.min()}")
print(f"  Max      : {scores.max()}")
print(f"  Range    : {scores.max() - scores.min()}")
print(f"  r (study vs score) : {r_numpy:.4f}")

plt.ioff()
plt.show()