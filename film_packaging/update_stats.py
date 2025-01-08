import os
import sys
import datetime
from shared import *

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


def replace_lines(filename):
	in_file = open(filename, encoding='utf8')
	text_lines = in_file.readlines()
	in_file.close()

	latest_scan = max([int(x[DATE_ADDED_KEY]) for x in database_entries])
	utc_datetime = datetime.datetime.fromtimestamp(latest_scan, datetime.timezone.utc)
	formatted_date = utc_datetime.strftime('%b %d %Y')

	LAST_UPDATED_STR = "Last Updated:"
	ITEMS_COUNT_STR = "# of items:"

	for index, line in enumerate(text_lines):
		if line.startswith(LAST_UPDATED_STR):
			text_lines[index] = f"{LAST_UPDATED_STR} {formatted_date}\n"
		if line.startswith(ITEMS_COUNT_STR):
			text_lines[index] = f"{ITEMS_COUNT_STR} {len(database_entries)}\n"

	out_file = open(filename, 'w', encoding='utf8')
	out_file.writelines(text_lines)
	out_file.close()

	print(f"Stats updated! {filename}")

replace_lines("../README.md")

replace_lines("./by_brand.md")