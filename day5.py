# Day 5: Dictionaries & Sets

# 1. Dictionary (Structured Key-Value Storage)
developer_profile = {
    "name": "Gaurav",
    "role": "Web Developer",
    "target_language": "Python"
}
# Accessing data using keys instead of index numbers
print(f"Developer Name: {developer_profile['name']}")
print(f"Target Focus: {developer_profile['target_language']}")

# 2. Sets (Ensuring Unique Values / Eliminating Duplicates)
# A raw data stream with accidental duplicates
raw_logins = ["Dhangadhi", "Kathmandu", "Dhangadhi", "Pokhara", "Kathmandu"]

# Converting the list to a set automatically discards duplicate values
unique_locations = set(raw_logins)
print(f"\nRaw Login Logs: {raw_logins}")
print(f"Cleaned Unique Locations: {unique_locations}")