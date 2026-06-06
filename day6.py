# 1. Basic comprehension — square numbers
squares = [x**2 for x in range(1, 11)]

# 2. Filtered comprehension — only evens
evens = [x for x in range(1, 21) if x % 2 == 0]

# 3. Rewrite a loop using comprehension
# Old way:
upper = []
for word in ["python", "data", "science"]:
    upper.append(word.upper())

# New way:
upper = [word.upper() for word in ["python", "data", "science"]]

# 4. enumerate — index tracking
topics = ["Variables", "Conditionals", "Lists", "Tuples", "Dicts", "Comprehensions"]
for i, topic in enumerate(topics, start=1):
    print(f"Day {i}: {topic}")

# 5. Combine both — comprehension with enumerate
indexed = [f"{i}. {topic}" for i, topic in enumerate(topics, start=1)]