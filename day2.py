# Day 2: Conditional Logic & Operators in Action

# example data input
username = "Gaurav"
daily_study_minutes = 45
has_completed_day1 = True

print(f"--- Running Profile Evaluation for {username} ---")

# 1. Combining Logical Operators (and, or) & Relational Operators (>==)
if daily_study_minutes >= 30 and has_completed_day1:
    print("Status: Streak Active! Momentum is looking solid.")
    
# 2. Using if/elif/else conditional blocks
elif daily_study_minutes < 30 and daily_study_minutes > 0:
    print("Status: Warning. Short study session detected. Keep pushing!")
    
else:
    print("Status: Streak at risk. Complete your daily block!")

# 3. Quick Arithmetic Operator Example (Modulo)
# Checking if the study time is an even or odd number
if daily_study_minutes % 2 == 0:
    print("Metric: Daily study minutes are an even number.")
else:
    print("Metric: Daily study minutes are an odd number.")