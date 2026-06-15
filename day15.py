import json
import os
import datetime

# ---- config ----
INPUT_FILE  = "menu.json"
OUTPUT_FILE = "clean_menu.json"
LOG_FILE    = "validation_log.txt"

now = datetime.datetime.now()

# ---- load raw JSON ----
def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"'{path}' not found.")
    with open(path, "r") as f:
        return json.load(f)

# ---- validate a single item — returns list of errors found ----
def validate_item(item):
    errors = []
    if item["price"] <= 0:
        errors.append(f"invalid price ({item['price']})")
    if not (0 <= item["popularity_score"] <= 100):
        errors.append(f"popularity out of range ({item['popularity_score']})")
    if not isinstance(item["in_stock"], bool):
        errors.append("in_stock must be boolean")
    return errors

# ---- validate all items, split into clean and flagged ----
def validate_all(data):
    clean   = []
    flagged = []
    for item in data:
        errors = validate_item(item)
        if errors:
            flagged.append({**item, "errors": errors})
        else:
            clean.append(item)
    return clean, flagged

# ---- filter clean data ----
def filter_data(clean, category=None, min_score=0, in_stock_only=False):
    result = clean
    if category:
        result = [i for i in result if i["category"].lower() == category.lower()]
    if in_stock_only:
        result = [i for i in result if i["in_stock"]]
    result = [i for i in result if i["popularity_score"] >= min_score]
    return result

# ---- write validation log ----
def write_log(data, clean, flagged, filtered):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"{'='*55}\n")
        f.write(f"  CLI Menu Data Logger\n")
        f.write(f"  Run at : {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*55}\n\n")

        f.write(f"  Total loaded  : {len(data)}\n")
        f.write(f"  Clean         : {len(clean)}\n")
        f.write(f"  Flagged       : {len(flagged)}\n")
        f.write(f"  After filter  : {len(filtered)}\n\n")

        if flagged:
            f.write(f"--- Flagged Items ---\n")
            for item in flagged:
                f.write(f"  [FLAGGED] {item['name']} -> {', '.join(item['errors'])}\n")

        f.write(f"\n--- Filtered Results ---\n")
        for item in filtered:
            stock = "IN STOCK" if item["in_stock"] else "OUT OF STOCK"
            f.write(f"  {item['name']:<22} | ${item['price']:.2f} | score: {item['popularity_score']} | {stock}\n")

# ---- save clean filtered data ----
def save_output(filtered):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(filtered, f, indent=2)

# ---- display results in terminal ----
def display(data, clean, flagged, filtered):
    print(f"\n{'='*55}")
    print(f"  📦 Raw loaded     : {len(data)} items")
    print(f"  ✅ Clean          : {len(clean)} items")
    print(f"  ❌ Flagged        : {len(flagged)} items")
    print(f"{'='*55}")

    if flagged:
        print(f"\n⚠️  Validation Errors:")
        for item in flagged:
            print(f"  ❌ {item['name']} → {', '.join(item['errors'])}")

    print(f"\n📋 Filtered Results ({len(filtered)} items):\n")
    print(f"  {'Name':<22} {'Category':<10} {'Price':>7}  {'Score':>6}  Stock")
    print(f"  {'-'*22} {'-'*10} {'-'*7}  {'-'*6}  {'-'*5}")
    for item in filtered:
        stock = "✅" if item["in_stock"] else "❌"
        print(f"  {item['name']:<22} {item['category']:<10} ${item['price']:>6.2f}  {item['popularity_score']:>6}  {stock}")

# ---- main CLI ----
def main():
    print(f"\n{'='*55}")
    print(f"  🍽️  Menu Data Logger — Milestone 1")
    print(f"{'='*55}")

    # load
    data = load_json(INPUT_FILE)
    print(f"\n✅ Loaded {len(data)} items from '{INPUT_FILE}'")

    # validate
    clean, flagged = validate_all(data)

    # get filter preferences from user
    print(f"\n--- Filters ---")
    category     = input("Filter by category (Main/Side/Dessert or leave blank): ").strip()
    min_score    = input("Minimum popularity score (0–100, default 0): ").strip()
    in_stock_only = input("In-stock items only? (y/n): ").strip().lower()

    min_score     = float(min_score) if min_score else 0
    in_stock_only = in_stock_only == "y"

    # filter
    filtered = filter_data(clean, category or None, min_score, in_stock_only)

    # display
    display(data, clean, flagged, filtered)

    # save outputs
    save_output(filtered)
    write_log(data, clean, flagged, filtered)

    print(f"\n📁 Outputs saved:")
    print(f"  {OUTPUT_FILE:<25} {os.path.getsize(OUTPUT_FILE)} bytes")
    print(f"  {LOG_FILE:<25} {os.path.getsize(LOG_FILE)} bytes")

main()