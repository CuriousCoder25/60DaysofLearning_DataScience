import csv
import json
import os

# ---- PART 1: writing a CSV ----
# csv.writer handles commas, quotes, escaping — don't do this manually
headers = ["name", "age", "city", "score"]
students = [
    ["Gaurav",  21, "Kathmandu", 88],
    ["Alice",   22, "Pokhara",   92],
    ["Bob",     20, "Dhangadhi", 75],
    ["Diana",   23, "Butwal",    95],
    ["Eve",     21, "Biratnagar",81],
]

with open("students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)       # write header row first
    writer.writerows(students)     # write all rows at once

print("✅ students.csv written\n")

# ---- PART 2: reading a CSV ----
# csv.DictReader maps each row to a dict using the header as keys
# much cleaner than indexing by position like row[0], row[1]
print("📄 Reading students.csv:\n")
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['name']:<10} | age: {row['age']} | city: {row['city']} | score: {row['score']}")

# ---- PART 3: converting CSV data to JSON ----
# this is a very common real pipeline step —
# ingest CSV, convert to JSON for an API or downstream process
print("\n🔄 Converting CSV → JSON...\n")
data = []
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # cast types — everything from CSV comes in as a string
        row["age"] = int(row["age"])
        row["score"] = int(row["score"])
        data.append(row)

# json.dump writes to file, indent=2 makes it human-readable
with open("students.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ students.json written\n")

# ---- PART 4: reading JSON back ----
# json.load deserializes the file back into Python dicts/lists
print("📄 Reading students.json:\n")
with open("students.json", "r") as f:
    loaded = json.load(f)

for student in loaded:
    stars = "★" * (student["score"] // 20) + "☆" * (5 - student["score"] // 20)
    print(f"  {student['name']:<10} | {student['city']:<12} | {stars}")

# ---- PART 5: filter high scorers and export as new JSON ----
# simulates a real pipeline step — filter, transform, export
print("\n🏆 High scorers (score >= 85):\n")
high_scorers = [s for s in loaded if s["score"] >= 85]

with open("high_scorers.json", "w") as f:
    json.dump(high_scorers, f, indent=2)

for s in high_scorers:
    print(f"  {s['name']} — {s['score']}")

print(f"\n✅ {len(high_scorers)} high scorers saved to high_scorers.json")
print(f"\n📦 Files created:")
for fname in ["students.csv", "students.json", "high_scorers.json"]:
    print(f"  {fname} — {os.path.getsize(fname)} bytes")