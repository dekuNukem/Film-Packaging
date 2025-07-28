import os
import sys
import datetime
from shared import *
from collections import Counter

def print_ranked_counts(counts):
    # Print headers
    print(f"{'Username':<20}{'Contributions':<20}")
    print('-' * 40)
    
    # Print each username and count
    for username, count in counts.items():
        print(f"{username:<20}{count:<20}")

def get_ranked_counts_string(counts):
    lines = []
    lines.append(f"{'Username':<20}{'Contributions':<20}")
    lines.append('-' * 40)
    for username, count in counts.items():
        lines.append(f"{username:<20}{count:<20}")
    return '\n'.join(lines)

database_entries = []

try:
    csv_file = open(database_csv_path)
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        database_entries.append(row)
    csv_file.close()
except Exception as e:
    print("csv read exception:", e)

convert_keys_to_int(database_entries)

authors_list = []
key_name = "author"
for item in database_entries:
	if key_name not in item:
		continue
	authors_list.append(item[key_name])

result = Counter(authors_list)
sorted_counts = Counter(dict(sorted(result.items(), key=lambda x: x[1], reverse=True)))
# print_ranked_counts(sorted_counts)


sdfsdfsd = get_ranked_counts_string(sorted_counts)
print(sdfsdfsd)

