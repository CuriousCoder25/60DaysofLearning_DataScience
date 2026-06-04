# Day 4: Data Collections - Tuples & For Loops

# 1. Defining an Immutable Tuple (e.g., coordinates or fixed constants)
# Unlike lists, tuples use parentheses () and cannot be modified after creation
fixed_geo_coordinates = (28.684, 80.612) 
print(f"Fixed Coordinates: {fixed_geo_coordinates}")

# Trying to change a tuple element like: fixed_geo_coordinates[0] = 29.0 
# will throw a TypeError. This protects critical data from accidental corruption.

# 2. Iterating through data using a 'for' loop
daily_study_hours = [1.2, 2.5, 1.8, 3.0, 2.2]
total_hours = 0.0

print("\n--- Iterating Through Study Log ---")
for hours in daily_study_hours:
    print(f"Recorded Session: {hours} hours")
    total_hours += hours  # Aggregating the data points

print(f"\nTotal Accumulated Study Time: {total_hours} hours")