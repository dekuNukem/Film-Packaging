import os
import sys
import datetime
from shared import *
from collections import Counter

def make_contributor_list(sorted_count_result):
    # Calculate the maximum username length and add 5
    max_username_length = max(len(username) for username in sorted_count_result.keys()) + 5
    
    lines = []
    lines.append(f"{'Rank':<6}{'Username':<{max_username_length}}{'Contributions':<6}")
    lines.append('-' * (max_username_length + 20))
    
    for rank, (username, count) in enumerate(sorted_count_result.items(), start=1):
        lines.append(f"{rank:<6}{username:<{max_username_length}}{count:<6}")
    
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
unique_film_count = 0
for item in database_entries:
	authors_list.append(item[ITEM_AUTHOR_KEY])
	if item[ITEM_SUBINDEX_KEY] == 0:
		unique_film_count += 1

result = Counter(authors_list)
sorted_counts = Counter(dict(sorted(result.items(), key=lambda x: x[1], reverse=True)))

def replace_lines(filename):
	in_file = open(filename, encoding='utf8')
	text_lines = in_file.readlines()
	in_file.close()

	latest_scan = max([int(x[DATE_ADDED_KEY]) for x in database_entries])
	utc_datetime = datetime.datetime.fromtimestamp(latest_scan, datetime.timezone.utc)
	formatted_date = utc_datetime.strftime('%b %d %Y')

	LAST_UPDATED_STR = "Last Updated:"
	UNIQUE_ITEM_STR = "Unique items:"
	TOTAL_SCAN_COUNT_STR = "Total scans :"
	CONTRIBUTOR_LIST_STR = "## Contributor List"

	clean_lines = []
	is_in_cl = False
	backtick_count = 0
	for line in text_lines:
		if line.startswith(CONTRIBUTOR_LIST_STR):
			clean_lines.append(CONTRIBUTOR_LIST_STR)
			is_in_cl = True
		if is_in_cl and line.startswith("```"):
			backtick_count += 1
		if backtick_count == 2:
			is_in_cl = False
			backtick_count = 99
			continue
		if is_in_cl is False:
			clean_lines.append(line)

	# for item in clean_lines:
	# 	print(item)
	# exit()

	output_lines = []

	for line in clean_lines:
		if line.startswith(LAST_UPDATED_STR):
			output_lines.append(f"{LAST_UPDATED_STR} {formatted_date}\n")
		elif line.startswith(TOTAL_SCAN_COUNT_STR):
			output_lines.append(f"{TOTAL_SCAN_COUNT_STR} {len(database_entries)}\n")
		elif line.startswith(UNIQUE_ITEM_STR):
			output_lines.append(f"{UNIQUE_ITEM_STR} {unique_film_count}\n")
		elif line.startswith(CONTRIBUTOR_LIST_STR):
			output_lines.append(f"{CONTRIBUTOR_LIST_STR}\n\n```\n{make_contributor_list(sorted_counts)}\n```\n")
		else:
			output_lines.append(line)

	out_file = open(filename, 'w', encoding='utf8')
	out_file.writelines(output_lines)
	out_file.close()

	print(f"Stats updated! {filename}")

replace_lines("../README.md")

matching_files = [filename for filename in os.listdir('.') if os.path.isfile(filename) and filename.startswith('by_') and filename.endswith('.md')]

for item in matching_files:
	replace_lines(item)