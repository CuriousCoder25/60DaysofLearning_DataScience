import os
import datetime

now = datetime.datetime.now()

# ---- PART 1: datetime basics ----
print(f"Right now   : {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Day of week : {now.strftime('%A')}")
print(f"Year        : {now.year}\n")

# ---- PART 2: os basics ----
print(f"Current directory : {os.getcwd()}")
print(f"Files here        : {os.listdir('.')}\n")

# ---- PART 3: dataset scanner ----
# take the folder path from user — flexible, works anywhere on your machine
folder_input = input("Enter path to your datasets folder: ").strip()

# os.path.expanduser handles ~ in paths (e.g. ~/Downloads/datasets)
datasets_folder = os.path.expanduser(folder_input)

# check it actually exists before trying to scan
if not os.path.exists(datasets_folder):
    print(f"\n Folder not found: '{datasets_folder}'")
    print("Double check the path and try again.")
else:
    print(f"\n Dataset Scan Report")
    print(f"Scanned at : {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Location   : {datasets_folder}\n")

    found = False
    for file in os.listdir(datasets_folder):
        if file.endswith(".csv") or file.endswith(".json"):
            found = True
            full_path = os.path.join(datasets_folder, file)
            size = os.path.getsize(full_path)
            modified = datetime.datetime.fromtimestamp(
                os.path.getmtime(full_path)
            ).strftime('%Y-%m-%d %H:%M')
            print(f"  {file}")
            print(f"    size     : {size} bytes")
            print(f"    modified : {modified}\n")


    if not found:
        print("  No CSV or JSON files found in this folder.")
        # The datasets are from kaggle : https://www.kaggle.com/competitions/titanic/data , shoutout to kaggle.
