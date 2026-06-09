# 1. Default parameters — if you don't pass a role, it just uses "Learner"
def greet(name, role="Learner"):
    return f"{name} — {role}"

print(greet("Gaurav"))                    # uses default
print(greet("Gaurav", "Data Scientist"))  # overrides default

# 2. *args — when you don't know how many values are coming in
# the * packs all positional arguments into a tuple
def total_score(*scores):
    print(f"Scores received: {scores}")   # it's just a tuple!
    return sum(scores)

print(total_score(85, 90, 78, 92))        # pass as many as you want

# 3. **kwargs — same idea but for named/keyword arguments
# the ** packs them into a dictionary
def build_profile(**details):
    for key, value in details.items():
        print(f"{key}: {value}")

# call it with whatever keys you feel like — totally flexible
build_profile(name="Gaurav", role="Developer", language="Python", day=9)

# 4. Combining all three — title is fixed, values are *args,
# decimals is a default param, extra info goes into **kwargs
def data_summary(title, *values, decimals=2, **metadata):
    avg = round(sum(values) / len(values), decimals)
    print(f"\n--- {title} ---")
    print(f"Average: {avg}")
    for key, value in metadata.items():   # print whatever extra info was passed
        print(f"{key}: {value}")

data_summary(
    "Score Report",
    85, 90, 78, 92, 88,   # these get packed into *values
    decimals=1,            # overrides the default 2
    subject="Python",      # these go into **metadata
    learner="Gaurav"
)