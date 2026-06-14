import datetime
import os
import json

now = datetime.datetime.now()

ENTRIES_FILE = "learning_entries.json"
LOG_FILE = "learning_log.txt"

# ---- load existing entries from JSON if file exists ----
# persists data between runs — not just a one-shot script
def load_entries():
    if os.path.exists(ENTRIES_FILE):
        with open(ENTRIES_FILE, "r") as f:
            return json.load(f)
    return []

# ---- save entries back to JSON ----
def save_entries(entries):
    with open(ENTRIES_FILE, "w") as f:
        json.dump(entries, f, indent=2)

# ---- append a single entry to the text log ----
def append_to_log(entry):
    stars = "★" * entry["rating"] + "☆" * (5 - entry["rating"])
    tag = "✅" if entry["status"] == "done" else "⏳"
    with open(LOG_FILE, "a") as f:
        f.write(f"  {tag} Day {entry['day']:>2} | {entry['topic']:<28} | {stars} | {entry['note']}\n")

# ---- rewrite the full log from scratch ----
# called after edits or deletions so the file stays in sync
def rebuild_log(entries):
    with open(LOG_FILE, "w") as f:
        f.write(f"{'='*70}\n")
        f.write(f"  60 Days of Learning — Progress Log\n")
        f.write(f"  Last updated : {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*70}\n\n")
        for entry in entries:
            stars = "★" * entry["rating"] + "☆" * (5 - entry["rating"])
            tag = "✅" if entry["status"] == "done" else "⏳"
            f.write(f"  {tag} Day {entry['day']:>2} | {entry['topic']:<28} | {stars} | {entry['note']}\n")
        done = sum(1 for e in entries if e["status"] == "done")
        f.write(f"\n{'='*70}\n")
        f.write(f"  Progress : {done}/{len(entries)} days completed\n")
        f.write(f"{'='*70}\n")

# ---- add a new day entry interactively ----
def add_entry(entries):
    print("\n--- Add New Entry ---")
    day = int(input("Day number : ").strip())

    # check if day already exists
    if any(e["day"] == day for e in entries):
        print(f"⚠️  Day {day} already exists. Use edit instead.")
        return entries

    topic = input("Topic      : ").strip()
    status = input("Status (done/pending) : ").strip().lower()
    rating = int(input("Rating (1–5) : ").strip())
    note = input("Note       : ").strip()

    entry = {
        "day": day,
        "topic": topic,
        "status": status,
        "rating": rating,
        "note": note,
        "logged_at": now.strftime("%Y-%m-%d %H:%M:%S")
    }

    entries.append(entry)
    entries.sort(key=lambda x: x["day"])  # keep sorted by day number
    append_to_log(entry)
    save_entries(entries)
    print(f"✅ Day {day} logged.")
    return entries

# ---- edit an existing entry ----
def edit_entry(entries):
    print("\n--- Edit Entry ---")
    day = int(input("Which day to edit? : ").strip())
    match = next((e for e in entries if e["day"] == day), None)

    if not match:
        print(f"⚠️  Day {day} not found.")
        return entries

    print(f"Current topic  : {match['topic']}")
    print(f"Current status : {match['status']}")
    print(f"Current rating : {match['rating']}")
    print(f"Current note   : {match['note']}")

    # only update fields the user actually types something for
    new_topic  = input("New topic  (enter to keep) : ").strip()
    new_status = input("New status (enter to keep) : ").strip()
    new_rating = input("New rating (enter to keep) : ").strip()
    new_note   = input("New note   (enter to keep) : ").strip()

    if new_topic:  match["topic"]  = new_topic
    if new_status: match["status"] = new_status
    if new_rating: match["rating"] = int(new_rating)
    if new_note:   match["note"]   = new_note

    rebuild_log(entries)
    save_entries(entries)
    print(f"✅ Day {day} updated.")
    return entries

# ---- view the full log in terminal ----
def view_log():
    if not os.path.exists(LOG_FILE):
        print("⚠️  No log file found yet.")
        return
    print()
    with open(LOG_FILE, "r") as f:
        # read line by line — good practice for large files
        for line in f:
            print(line, end="")
    print()

# ---- show summary stats ----
def show_stats(entries):
    if not entries:
        print("No entries yet.")
        return
    done    = [e for e in entries if e["status"] == "done"]
    pending = [e for e in entries if e["status"] == "pending"]
    avg_rating = sum(e["rating"] for e in done) / len(done) if done else 0
    top = max(done, key=lambda x: x["rating"]) if done else None

    print(f"\n--- Stats ---")
    print(f"  Total logged  : {len(entries)}")
    print(f"  Completed     : {len(done)}")
    print(f"  Pending       : {len(pending)}")
    print(f"  Avg rating    : {avg_rating:.1f} / 5.0")
    if top:
        print(f"  Top rated day : Day {top['day']} — {top['topic']} ({'★' * top['rating']})")

# ---- main menu loop ----
def main():
    entries = load_entries()

    # build log file fresh on startup if it doesn't exist
    if not os.path.exists(LOG_FILE):
        rebuild_log(entries)

    while True:
        print("\n╔══════════════════════════════╗")
        print("║   60 Days Learning Logger    ║")
        print("╠══════════════════════════════╣")
        print("║  1. Add entry                ║")
        print("║  2. Edit entry               ║")
        print("║  3. View full log            ║")
        print("║  4. Stats                    ║")
        print("║  5. Exit                     ║")
        print("╚══════════════════════════════╝")

        choice = input("Choice : ").strip()

        if choice == "1":
            entries = add_entry(entries)
        elif choice == "2":
            entries = edit_entry(entries)
        elif choice == "3":
            view_log()
        elif choice == "4":
            show_stats(entries)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice — pick 1–5.")

main()