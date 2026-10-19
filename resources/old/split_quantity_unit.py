import re
import csv
from shared import *

# One-off conversion: split "36exp" / "12 Sheets" / "7.5m" in the quantity column
# into quantity ("36") and unit ("exp"). Non-numeric values like N/A and Unknown
# are kept as-is in quantity with an empty unit. Safe to run more than once.

quantity_regex = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*([A-Za-z]+)\s*$")

database_entries = []

try:
    csv_file = open(database_csv_path)
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        database_entries.append(row)
    csv_file.close()
except Exception as e:
    print("csv read exception:", e)
    exit()

def split_quantity(entry):
    old_quantity = entry[ITEM_QUANTITY_KEY].strip()
    old_unit = entry.get(ITEM_UNIT_KEY, "").strip()
    if is_number(old_quantity):
        return old_quantity, old_unit
    match = quantity_regex.match(old_quantity)
    if match is None:
        return old_quantity, ""
    return match.group(1), match.group(2).lower()

unparsed = set()
new_entries = []

for entry in database_entries:
    quantity, unit = split_quantity(entry)
    if is_number(quantity) is False:
        unparsed.add(quantity)
    # rebuild dict so unit sits right after quantity in the csv
    new_entry = {}
    for key in entry:
        if key == ITEM_UNIT_KEY:
            continue
        new_entry[key] = entry[key]
        if key == ITEM_QUANTITY_KEY:
            new_entry[ITEM_QUANTITY_KEY] = quantity
            new_entry[ITEM_UNIT_KEY] = unit
    new_entries.append(new_entry)

save_csv(new_entries)

print(f"Converted {len(new_entries)} entries")
print(f"Non-numeric quantities kept as-is (unit left empty): {sorted(unparsed)}")
