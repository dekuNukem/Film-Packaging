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

def make_alt_text(this_entry):
    return f"{this_entry[ITEM_BRAND_KEY]} {this_entry[ITEM_PRODUCT_NAME_KEY]} {this_entry[ITEM_FORMAT_KEY]} {this_entry[ITEM_TYPE_KEY]}"

def make_subtitle(this_entry):
    return f"{this_entry[ITEM_BRAND_KEY]} {this_entry[ITEM_PRODUCT_NAME_KEY]} (ref: {this_entry[ITEM_UUID_KEY][-4:]})"

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

convert_keys_to_int(database_entries)
result = sorted(database_entries, key=operator.itemgetter(ITEM_BRAND_KEY, ITEM_PRODUCT_NAME_KEY, ITEM_INDEX_KEY, ITEM_SUBINDEX_KEY))

md_header = """# Film Packaging Archive (Sorted by BRAND)

[Project Home Page](../README.md)

-----

Find this useful? Please [credit the project page](https://github.com/dekuNukem/Film-Packaging)!

Want to contribute? [Check out the guidelines!](../contribution_guide.md)

👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇

🔎🔎 **CLICK IMAGE FOR FULL SIZE** 🔍🔍

☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️

```
Last Updated: 

# of items: 
```

-----

"""

print(md_header)

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

# [![Alt text](resources/title.jpg)](https://example.com)


for item in result:
    image_path = make_filename_full_path(item)
    lowres_path = make_lowres_full_path(item)
    description = ""
    if int(item[ITEM_SUBINDEX_KEY]) == 0:
        description += f"#### {make_subtitle(item)}"
        description += "\n```\n"
        description += make_description_string(item, ITEM_ISO_KEY)
        description += make_description_string(item, ITEM_FORMAT_KEY)
        description += make_description_string(item, ITEM_PROCESS_KEY)
        description += make_description_string(item, ITEM_EXPIRY_KEY)
        description += make_description_string(item, ITEM_UUID_KEY)
        description += make_description_string(item, ITEM_AUTHOR_KEY)
        description += "```\n"
        description += f"\n[![{make_alt_text(item)}]({lowres_path})]({image_path})\n"
    elif 'inside' in item[ITEM_TYPE_KEY].lower():
        description += f"[Click me for **BOX INSIDE** for {make_subtitle(item)}]({image_path})\n"
    elif 'leaflet' in item[ITEM_TYPE_KEY].lower():
        description += f"[Click me for **LEAFLET** for {make_subtitle(item)}]({image_path})\n"
    elif 'envelope' in item[ITEM_TYPE_KEY].lower():
        description += f"[Click me for **PROCESSING ENVELOPE** for {make_subtitle(item)}]({image_path})\n"
    else:
        description += f"\n[![{make_alt_text(item)}]({lowres_path})]({image_path})\n"

    print(description)
    
ending = """

## Want to contribute?

[Check out the guidelines!](../contribution_guide.md)

## Questions or Comments?

Get in touch by joining [the Discord chatroom](https://discord.gg/yvBx7dVG4B), or `email skate.huddle-6r@icloud.com` !

## Back to Main Page

[Click me](../README.md)

"""

print(ending)