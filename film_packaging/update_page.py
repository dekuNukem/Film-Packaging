import os
import sys
import csv
import time
from shared import *
import operator

# Enforce UTF-8 for consistency across terminals
sys.stdout.reconfigure(encoding='utf-8')

def make_description_string(this_entry, keyname):
    if keyname not in this_entry:
        raise ValueError()
    attri_disp_name = find_key_attributes(keyname).display_name
    return f"{attri_disp_name:8}: {this_entry[keyname]}\n"

def make_alt_text(this_entry):
    return f"{this_entry[ITEM_BRAND_KEY]} {this_entry[ITEM_PRODUCT_NAME_KEY]} {this_entry[ITEM_FORMAT_KEY]} {this_entry[ITEM_TYPE_KEY].replace("_", " ")}"

def make_subtitle(this_entry, foretext_key=None, foretext_func=None):
    front_bit = ""
    if foretext_key in this_entry:
        front_bit = f"{this_entry[foretext_key]}"
    if foretext_func is not None:
        front_bit = foretext_func(front_bit)
    if len(front_bit) > 0:
        front_bit = f"[{front_bit}] "
    return f"{front_bit}{this_entry[ITEM_BRAND_KEY]} {this_entry[ITEM_PRODUCT_NAME_KEY]} (ref: {this_entry[ITEM_UUID_KEY][-4:]})"

def make_lazy_load_image_link(this_lowres_path, this_image_path, this_entry):
    display_width, display_height = get_resized_dimensions(this_lowres_path, max_size=500)
    # output = f"\n<a href=\"{this_image_path}\">"
    output = f'\n<a href="{this_image_path}" target="_blank">'
    output += f"\n\t<img src=\"{this_lowres_path}\" alt=\"{make_alt_text(this_entry)}\" loading=\"lazy\" width=\"{display_width}\" height=\"{display_height}\">"
    output += f"\n</a>\n"
    return output

def make_section(text):
    placeholder = '$%'
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

def get_header(sorted_by_str):
    return f"""# Film Packaging Archive (Sorted by {sorted_by_str})

[Home Page](../README.md) | [GitHub Repo](https://github.com/dekuNukem/Film-Packaging)

-----

Find this useful? Please [credit the project page](../README.md)!

Want to contribute? [Check out the guidelines!](../contribution_guide.md)

👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇

🔎🔎 **CLICK IMAGE FOR FULL SIZE** 🔍🔍

☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️

```
Last Updated:
Unique items:
Total scans :
```

-----

"""

def get_ending():
    return """## Want to Contribute?

[Check out the guidelines!](../contribution_guide.md)

## Contributor List

```
```

## Questions or Comments?

Get in touch by joining [the Discord chatroom](https://discord.gg/yvBx7dVG4B), or `email skate.huddle-6r@icloud.com` !

## Back to Home Page

[Click me](../README.md)

"""

from datetime import datetime, UTC

def render_two_cols(info: dict, col_width: int = 21) -> str:
    # Parse/format dates
    exp = info.get("expiry_date", "")
    if len(exp) == 6 and exp.isdigit():
        exp_fmt = f"{exp[:4]}-{exp[4:]}"
    else:
        exp_fmt = exp  # fallback as-is

    try:
        ts = int(info.get("date_added", 0))
        added_fmt = datetime.fromtimestamp(ts, UTC).strftime("%Y-%m-%d")
    except Exception:
        added_fmt = ""

    # Field values
    fmt = info.get(ITEM_FORMAT_KEY, "")
    proc = info.get(ITEM_PROCESS_KEY, "")
    iso = info.get(ITEM_ISO_KEY, "")
    author = info.get(ITEM_AUTHOR_KEY, "")
    uuid = info.get(ITEM_UUID_KEY, "")
    box_type = info.get(ITEM_SUB_TYPE_KEY, "")
    quantity = info.get(ITEM_QUANTITY_KEY, "")
    notes = info.get(ITEM_NOTES_KEY, "")

    # Helper to make one column padded to col_width
    def col(label, value):
        return f"{label}: {value}".ljust(col_width)

    # Build the lines
    line1 = col("Format", fmt) + col("|  Process ", proc)
    line2 = col("ISO   ", iso) + col("|  Expiry  ", exp_fmt)
    line3 = col("Type  ", box_type) + col("|  Quantity", quantity)
    line4 = col("Added ", added_fmt) + col("|  Author  ", author)
    line5 = f"UUID  : {uuid}\n"
    return "\n".join([line1, line2, line3, line4, line5])

# -----------

def make_md(sort_name, sorted_dbase, ftk=None, ftf=None):
    result_text = ""
    result_text += get_header(sort_name)
    subtitle_list = []

    for item in sorted_dbase:
        if item[ITEM_SUBINDEX_KEY] != 0:
            continue
        this_subtitle = make_subtitle(item, foretext_key=ftk, foretext_func=ftf)
        if this_subtitle not in subtitle_list:
            subtitle_list.append(this_subtitle)

    for item in subtitle_list:
        result_text += make_section(item) + "\n"

    result_text += "\n\n-----\n\n"

    for item in sorted_dbase:
        image_path = make_filename_full_path(item)
        lowres_path = make_lowres_full_path(item)
        description = ""
        if int(item[ITEM_SUBINDEX_KEY]) == 0:
            description += f"#### {make_subtitle(item, foretext_key=ftk, foretext_func=ftf)}\n"
            description += "\n```\n"
            description += render_two_cols(item)
            description += "```\n"
            description += make_lazy_load_image_link(lowres_path, image_path, item)
        else:
            description += f"\n`UUID: {item[ITEM_UUID_KEY]}`↓\n"
            description += make_lazy_load_image_link(lowres_path, image_path, item)

        result_text += description + '\n'
        
    result_text += get_ending()
    return result_text

def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# ----------

def expiry_func(text):
    if text.isnumeric():
        return text[:4]
    return text

# ----------

database_entries = []

try:
    csv_file = open(database_csv_path)
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        database_entries.append(row)
    csv_file.close()
    convert_keys_to_int(database_entries)
except Exception as e:
    print("csv read exception:", e)

sorted_db = sorted(database_entries, key=operator.itemgetter(ITEM_BRAND_KEY, ITEM_PRODUCT_NAME_KEY, ITEM_EXPIRY_KEY, ITEM_INDEX_KEY, ITEM_SUBINDEX_KEY))
out_str = make_md("BRAND", sorted_db)
write_to_file("./by_brand.md", out_str)

sorted_db = sorted(database_entries, key=operator.itemgetter(ITEM_EXPIRY_KEY, ITEM_BRAND_KEY, ITEM_PRODUCT_NAME_KEY, ITEM_INDEX_KEY, ITEM_SUBINDEX_KEY))
out_str = make_md("EXPIRY DATE", sorted_db, ftk=ITEM_EXPIRY_KEY, ftf=expiry_func)
write_to_file("./by_expiry.md", out_str)

sorted_db = sorted(database_entries, key=operator.itemgetter(ITEM_FORMAT_KEY, ITEM_BRAND_KEY, ITEM_PRODUCT_NAME_KEY, ITEM_EXPIRY_KEY, ITEM_INDEX_KEY, ITEM_SUBINDEX_KEY))
out_str = make_md("FILM FORMAT", sorted_db, ftk=ITEM_FORMAT_KEY, ftf=None)
write_to_file("./by_format.md", out_str)

sorted_db = sorted(database_entries, key=operator.itemgetter(ITEM_PROCESS_KEY, ITEM_BRAND_KEY, ITEM_PRODUCT_NAME_KEY, ITEM_EXPIRY_KEY, ITEM_INDEX_KEY, ITEM_SUBINDEX_KEY))
out_str = make_md("PROCESS TYPE", sorted_db, ftk=ITEM_PROCESS_KEY, ftf=None)
write_to_file("./by_process.md", out_str)

sorted_db = sorted(database_entries, key=operator.itemgetter(ITEM_AUTHOR_KEY, ITEM_BRAND_KEY, ITEM_PRODUCT_NAME_KEY, ITEM_EXPIRY_KEY, ITEM_INDEX_KEY, ITEM_SUBINDEX_KEY))
out_str = make_md("CONTRIBUTOR", sorted_db, ftk=ITEM_AUTHOR_KEY, ftf=None)
write_to_file("./by_user.md", out_str)

from datetime import datetime

def timestamp_to_date(ts):
    try:
        ts = int(ts)
        if not isinstance(ts, (int, float)) or ts <= 0:
            return "unknown"
        return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")
    except Exception:
        return "unknown"

sorted_db = sorted(database_entries, key=operator.itemgetter(DATE_ADDED_KEY, ITEM_AUTHOR_KEY, ITEM_BRAND_KEY, ITEM_PRODUCT_NAME_KEY, ITEM_EXPIRY_KEY, ITEM_INDEX_KEY, ITEM_SUBINDEX_KEY), reverse=True)
out_str = make_md("DATE ADDED", sorted_db, ftk=DATE_ADDED_KEY, ftf=timestamp_to_date)
write_to_file("./by_recent.md", out_str)
