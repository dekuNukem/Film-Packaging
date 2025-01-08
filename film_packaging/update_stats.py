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
	readme_file = open(filename, encoding='utf8')
	readme_lines = readme_file.readlines()
	readme_file.close()

	latest_scan = max([int(x[DATE_ADDED_KEY]) for x in database_entries])
	utc_datetime = datetime.datetime.fromtimestamp(latest_scan, datetime.timezone.utc)
	formatted_date = utc_datetime.strftime('%b %d %Y')

	LAST_UPDATED_STR = "Last Updated:"
	ITEMS_COUNT_STR = "# of items:"

	for index, line in enumerate(readme_lines):
		if line.startswith(LAST_UPDATED_STR):
			readme_lines[index] = f"{LAST_UPDATED_STR} {formatted_date}"
		if line.startswith(ITEMS_COUNT_STR):
			readme_lines[index] = f"{ITEMS_COUNT_STR} {len(database_entries)}"

	for item in readme_lines:
		print(item)


replace_lines("../README.md")