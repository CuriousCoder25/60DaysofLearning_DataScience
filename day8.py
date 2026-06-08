# 1. Basic function with return
def greet(name):
    return f"Hello, {name}!"

print(greet("Gaurav")) #function call

# 2. Local vs global scope
total = 0  # global

def add_to_total(points):
    local_tax = 0.1  # local -- dies after function ends
    return total + points + (points * local_tax)

print(add_to_total(50))

# 3. A small data pipeline -- functions calling functions
def clean_name(name):
    return name.strip().title()

def build_profile(name, role, language):
    return {
        "name": clean_name(name),
        "role": role,
        "language": language
    }

def display_profile(profile):
    for key, value in profile.items():
        print(f"{key.upper()}: {value}")

profile = build_profile("  gaurav  ", "Developer", "Python")
display_profile(profile)