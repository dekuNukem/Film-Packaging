import os
import sys
import csv
import time
from shared import *
import operator

def make_description_string(this_entry, keyname):
    if keyname not in this_entry:
        raise ValueError()
    attri_disp_name = find_key_attributes(keyname).display_name
    return f"{attri_disp_name:8}: {item[keyname]}\n"

def make_subtitle(this_entry):
    return f"{this_entry[ITEM_BRAND_KEY]} {item[ITEM_PRODUCT_NAME_KEY]} (ref: {item[ITEM_UUID_KEY][-4:]})"

placeholder = '$%'
def make_section(text):
    text = text.lstrip("#").replace('\r', '').replace('\n', '').strip()
    link = text.lower().replace('.', '')
    result = ''
    for letter in link:
        if letter.isalnum() or letter == '_':
            result += letter
        elif letter == '/':
            result += placeholder
        elif letter == '\'':
            continue
        else:
            result += '-'
    while '--' in result:
        result = result.replace('--', '-')
    result = result.strip('-')
    result = result.replace(placeholder, '')
    return f'- [{text}](#{result})'

# ----------

database_entries = []

try:
    csv_file = open(database_csv_path)
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        database_entries.append(row)
    csv_file.close()
except Exception as e:
    print("csv read exception:", e)

for this_entry in database_entries:
    this_entry[ITEM_INDEX_KEY] = int(this_entry[ITEM_INDEX_KEY])
    this_entry[ITEM_SUBINDEX_KEY] = int(this_entry[ITEM_SUBINDEX_KEY])

result = sorted(database_entries, key=operator.itemgetter(ITEM_BRAND_KEY, ITEM_PRODUCT_NAME_KEY, ITEM_INDEX_KEY, ITEM_SUBINDEX_KEY))

subtitle_list = []

for item in result:
    if item[ITEM_SUBINDEX_KEY] != 0:
        continue
    this_subtitle = make_subtitle(item)
    if this_subtitle not in subtitle_list:
        subtitle_list.append(this_subtitle)

for item in subtitle_list:
    print(make_section(item))

print("\n\n-----\n\n")

for item in result:
    image_path = make_filename(item)
    description = ""
    if int(item[ITEM_SUBINDEX_KEY]) == 0:
        description += f"#### {make_subtitle(item)}"
        description += "\n```\n"
        description += make_description_string(item, ITEM_ISO_KEY)
        description += make_description_string(item, ITEM_FORMAT_KEY)
        description += make_description_string(item, ITEM_PROCESS_KEY)
        description += make_description_string(item, ITEM_EXPIRY_KEY)
        description += make_description_string(item, ITEM_UUID_KEY)
        description += "```\n"
    description += f"\n![alt_text]({image_path})\n"

    print(description)
    