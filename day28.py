import pandas as pd

students = pd.DataFrame({
    "name": ["Gaurav", "Alice", "Bob", "Diana", "Eve"],
    "age": [21, 22, 20, 23, 21],
    "city": ["Kathmandu", "Pokhara", "Dhangadhi", "Butwal", "Biratnagar"],
    "score": [88, 92, 75, 95, 81]
})
print(f"DataFrame:\n{students}\n")

# THE CORE RULE TO REMEMBER:
# .iloc = INTEGER location, pure position, like list indexing.
# .loc  = LABEL location, uses the actual index/column names.
# Mnemonic: "i" in iloc means integer/index position.
# "loc" alone means locate by LABEL, not position.

# .iloc[row, col] is purely positional, just like NumPy slicing
# from Day 18, but now on a DataFrame instead of a raw array.
print(f"First row (iloc[0])      :\n{students.iloc[0]}\n")
print(f"First 3 rows (iloc[0:3]) :\n{students.iloc[0:3]}\n")
print(f"Row 1, Col 0 (iloc[1,0]) : {students.iloc[1, 0]}")

# .loc uses the actual index label. Right now our index is just
# 0,1,2,3,4 (default), so it looks the same as iloc, but the
# moment we change the index, the difference becomes obvious.
print(f"\nRow with label 1 (loc[1]) :\n{students.loc[1]}\n")

# WHY THIS MATTERS: set 'name' as the actual index instead of
# the default 0,1,2... Now .loc can find rows by NAME, which
# .iloc can never do. iloc only ever understands position.
named_students = students.set_index("name")
print(f"Indexed by name:\n{named_students}\n")

print(f"Gaurav's row (loc['Gaurav'])     :\n{named_students.loc['Gaurav']}\n")
print(f"Gaurav's score (loc['Gaurav','score']) : {named_students.loc['Gaurav', 'score']}")

# IMPORTANT: set_index doesn't just relabel rows, it REMOVES
# that column from the regular column list entirely. The
# named_students DataFrame now only has 3 columns left:
# age (0), city (1), score (2). The "name" column is gone
# from the columns, since it became the index instead.
print(f"\nColumns after set_index : {list(named_students.columns)}")

# So Gaurav's score is now at position 2, not 3, because
# the column shifted left once "name" was removed.
print(f"Same thing via iloc (iloc[0,2]) : {named_students.iloc[0, 2]}")

# .loc with column names is genuinely more useful day to day.
# We rarely remember "column 2 is score," but we always know
# the column is literally named "score".
print(f"\nName + score only (.loc) :\n{named_students.loc[:, ['score']]}\n")

# SLICING DIFFERENCE THAT TRIPS PEOPLE UP:
# .iloc slicing EXCLUDES the end, just like Python lists.
# .loc slicing INCLUDES the end, because it matches a label, not a position.
print(f".iloc[0:2] (excludes index 2):\n{students.iloc[0:2]}\n")
print(f".loc[0:2] (includes index 2):\n{students.loc[0:2]}")