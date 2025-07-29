import os
import csv

ITEM_INDEX_KEY = 'index'
ITEM_SUBINDEX_KEY = 'sub_index'
ITEM_TYPE_KEY = 'item_type'
ITEM_UUID_KEY = "uuid"
DATE_ADDED_KEY = "date_added"

ITEM_BRAND_KEY = 'brand'
ITEM_PRODUCT_NAME_KEY = 'product'
ITEM_FORMAT_KEY = 'film_format'
ITEM_ISO_KEY = 'film_speed_iso'
ITEM_PROCESS_KEY = 'process'
ITEM_EXPIRY_KEY = 'expiry_date'
CHECKSUM_KEY = "md5"
ITEM_FILE_NAME_KEY = 'filename'
ITEM_AUTHOR_KEY = "author"
alert_color = 'cyan'

database_csv_path = "./database.csv"
ingest_dir_path = "./to_add"
archive_dir_path = "./archive"
lowres_dir_path = "./lowres"

AUTHOR_NAME_MYSELF = "dekuNukem"

class my_attribute:
    def __init__(self):
        self.db_name = ""
        self.display_name = ""
        self.no_need_to_ask = False
        self.list_existing = False
        self.notes = ""

    def __str__(self):
        return (
            f"db_name\t\t: {self.db_name}\n"
            f"display_name\t: {self.display_name}\n"
            f"no_need_to_ask\t: {self.no_need_to_ask}\n"
            f"list_existing\t: {self.list_existing}\n"
            f"notes\t\t: {self.notes}\n"
        )

record_key_list = []

this_key = my_attribute()
this_key.db_name = ITEM_INDEX_KEY
this_key.display_name = "Index"
this_key.no_need_to_ask = True
this_key.notes = ""
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = ITEM_SUBINDEX_KEY
this_key.display_name = ITEM_SUBINDEX_KEY
this_key.no_need_to_ask = True
this_key.list_existing = False
this_key.notes = "Default 0"
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = ITEM_TYPE_KEY
this_key.display_name = "Item Type"
this_key.no_need_to_ask = False
this_key.list_existing = True
this_key.notes = "single_box_outside, single_box_outside, leaflet, etc"
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = ITEM_BRAND_KEY
this_key.display_name = "Brand"
this_key.no_need_to_ask = False
this_key.list_existing = True
this_key.notes = ""
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = ITEM_PRODUCT_NAME_KEY
this_key.display_name = "Product"
this_key.no_need_to_ask = False
this_key.list_existing = True
this_key.notes = "e.g. Fujicolor Super HR, Etkachrome, Gold, etc"
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = ITEM_FORMAT_KEY
this_key.display_name = "Format"
this_key.no_need_to_ask = False
this_key.list_existing = True
this_key.notes = "35mm, 120, 4x5, etc."
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = ITEM_ISO_KEY
this_key.display_name = "ISO"
this_key.no_need_to_ask = False
this_key.list_existing = False
this_key.notes = ""
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = ITEM_PROCESS_KEY
this_key.display_name = "Process"
this_key.no_need_to_ask = False
this_key.list_existing = True
this_key.notes = "C41, E6, BW, ECN2, etc"
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = ITEM_EXPIRY_KEY
this_key.display_name = "Expiry"
this_key.no_need_to_ask = False
this_key.list_existing = False
this_key.notes = "YYYYMM"
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = DATE_ADDED_KEY
this_key.display_name = "Date Added"
this_key.no_need_to_ask = True
this_key.list_existing = False
this_key.notes = ""
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = CHECKSUM_KEY
this_key.display_name = "MD5"
this_key.no_need_to_ask = True
this_key.list_existing = False
this_key.notes = ""
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = ITEM_UUID_KEY
this_key.display_name = "UUID"
this_key.no_need_to_ask = True
this_key.notes = ""
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = ITEM_FILE_NAME_KEY
this_key.display_name = "File Name"
this_key.no_need_to_ask = True
this_key.notes = ""
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = ITEM_AUTHOR_KEY
this_key.display_name = "Scanned By"
this_key.no_need_to_ask = True
this_key.notes = ""
record_key_list.append(this_key)

def find_key_attributes(key_name_str):
    for item in record_key_list:
        if item.db_name == key_name_str:
            return item
    raise ValueError(f"Unknown key: {key_name_str}")

def make_filename_only(item_dict):
    return f"{int(item_dict[ITEM_INDEX_KEY]):05}_{int(item_dict[ITEM_SUBINDEX_KEY]):03}.jpg"

def make_filename_full_path(item_dict):
    new_filename = make_filename_only(item_dict)
    return os.path.join(archive_dir_path, new_filename).replace('\\', '/')

def make_lowres_full_path(item_dict):
    new_filename = make_filename_only(item_dict)
    return os.path.join(lowres_dir_path, new_filename).replace('\\', '/')

def convert_keys_to_int(db_dict):
    for this_entry in db_dict:
        this_entry[ITEM_INDEX_KEY] = int(this_entry[ITEM_INDEX_KEY])
        this_entry[ITEM_SUBINDEX_KEY] = int(this_entry[ITEM_SUBINDEX_KEY])

def save_csv(entries, csv_path=database_csv_path):
    csv_out_file = open(csv_path, 'w')
    csv_writer = csv.DictWriter(csv_out_file, fieldnames=entries[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(entries)
    csv_out_file.close()


from PIL import Image

def get_image_dimensions(file_path):
    try:
        with Image.open(file_path) as img:
            return img.width, img.height
    except Exception:
        return (0, 0)

def get_longest_side(file_path):
    width, height = get_image_dimensions(file_path)
    
    if width >= height:
        longest_side = "width"
        length = min(width, 500)
    else:
        longest_side = "height"
        length = min(height, 500)

    return longest_side, length
