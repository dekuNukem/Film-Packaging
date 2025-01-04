import os
import sys
import csv
import time
import uuid
from termcolor import colored
import psutil
import hashlib
from PIL import Image

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

ITEM_INDEX_KEY = 'index'
ITEM_SUBINDEX_KEY = 'sub_index'
ITEM_TYPE_KEY = 'item_type'
ITEM_UUID_KEY = "uuid"
DATE_ADDED_KEY = "date_added"
CHECKSUM_KEY = "md5"
alert_color = 'cyan'

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
this_key.db_name = 'brand'
this_key.display_name = "Brand"
this_key.no_need_to_ask = False
this_key.list_existing = True
this_key.notes = ""
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = 'product'
this_key.display_name = "Product"
this_key.no_need_to_ask = False
this_key.list_existing = True
this_key.notes = "e.g. Fujicolor Super HR, Etkachrome, Gold, etc"
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = 'film_format'
this_key.display_name = "Format"
this_key.no_need_to_ask = False
this_key.list_existing = True
this_key.notes = "35mm, 120, 4x5, etc."
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = 'film_speed_iso'
this_key.display_name = "ISO"
this_key.no_need_to_ask = False
this_key.list_existing = False
this_key.notes = ""
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = 'process'
this_key.display_name = "Process"
this_key.no_need_to_ask = False
this_key.list_existing = True
this_key.notes = "C41, E6, BW, ECN2, etc"
record_key_list.append(this_key)

this_key = my_attribute()
this_key.db_name = 'expiry_date'
this_key.display_name = "Expiry Date"
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

#-------

database_csv_path = "./database.csv"
ingest_dir_path = "./to_add"
database_entries = []

if os.path.isdir(ingest_dir_path) is False:
    print(f"'{ingest_dir_path}' is not a directory.")
    exit()

try:
    csv_file = open(database_csv_path)
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        database_entries.append(row)
    csv_file.close()
except Exception as e:
    print("csv read exception:", e)

print(database_entries)
# exit()

def get_md5_str(filepath):
    with open(filepath, "rb") as f:
        return hashlib.file_digest(f, "md5").hexdigest()

def is_file_already_in_db(entries, md5_str):
    for item in entries:
        if item[CHECKSUM_KEY] == md5_str:
            return True
    return False

def get_yn(question):
    while 1:
        response = input(f"{question}\n")
        if response.lower().startswith('y'):
            return True
        if response.lower().startswith('n'):
            return False

def get_answer(question, accept_empty=False):
    while True:
        response = input(f"{question}").strip()
        if accept_empty or len(response) > 0:
            return response

def ask_with_listing_existing_options(db_key):
    all_options = set()
    for item in database_entries:
        all_options.add(item[db_key])
    all_options = sorted([str(x) for x in all_options])
    option_list_str = ""
    for index, item in enumerate(all_options):
        option_list_str += f"{index}:  {item}\n"
    question_to_ask = f"\nWhat is {colored(db_key, alert_color)}?\nSelect existing option or type a new entry\n{option_list_str}"
    user_answer = get_answer(question_to_ask)
    try:
        return all_options[int(user_answer)]
    except Exception as e:
        # print("ask_with_listing_existing_options:", e)
        pass
    return user_answer

def ask_attribute(db_key):
    key_attri = find_key_attributes(db_key)
    if key_attri.no_need_to_ask:
        return
    if key_attri.list_existing:
        return ask_with_listing_existing_options(db_key)
    else:
        return get_answer(f"What is {colored(db_key, alert_color)}?\n")

def open_preview(filepath):
    os.system(f"open {filepath}")

def kill_preview():
    for proc in psutil.process_iter():
        if proc.name() == "Preview":
            proc.kill()

def get_empty_record():
    this_dict = {}
    for item in record_key_list:
        key_name = item.db_name
        this_dict[key_name] = ''
    return this_dict

def find_key_attributes(key_name_str):
    for item in record_key_list:
        if item.db_name == key_name_str:
            return item
    raise ValueError(f"Unknown key: {key_name_str}")

def build_record_from_scratch(filepath):
    this_record = get_empty_record()
    for keyname in this_record:
        this_record[keyname] = ask_attribute(keyname)

    try:
        this_record[ITEM_INDEX_KEY] = int(database_entries[-1][ITEM_INDEX_KEY]) + 1
    except Exception as e:
        print(e)
        this_record[ITEM_INDEX_KEY] = 0
    this_record[ITEM_SUBINDEX_KEY] = 0
    this_record[ITEM_UUID_KEY] = uuid.uuid4().hex
    this_record[DATE_ADDED_KEY] = int(time.time())
    this_record[CHECKSUM_KEY] = get_md5_str(filepath)

    return this_record

def build_record_from_existing(template, filepath):
    this_record = get_empty_record()
    for key in this_record:
        this_record[key] = template[key]
    this_record[ITEM_INDEX_KEY] = template[ITEM_INDEX_KEY]
    this_record[DATE_ADDED_KEY] = int(time.time())
    this_record[CHECKSUM_KEY] = get_md5_str(filepath)
    this_record[ITEM_UUID_KEY] = uuid.uuid4().hex
    this_record[ITEM_SUBINDEX_KEY] = int(this_record[ITEM_SUBINDEX_KEY]) + 1
    this_record[ITEM_TYPE_KEY] = ask_attribute(ITEM_TYPE_KEY)
    return this_record

def save_csv(entries):
    csv_out_file = open(database_csv_path, 'w')
    csv_writer = csv.DictWriter(csv_out_file, fieldnames=entries[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(entries)
    csv_out_file.close()

ingest_file_list = sorted(os.listdir(ingest_dir_path))

for fname in ingest_file_list:
    if fname.lower().endswith('.jpeg') is False:
        continue

    print(f"Processing {fname}...")
    this_file_path = os.path.join(ingest_dir_path, fname)
    this_md5 = get_md5_str(this_file_path)
    if is_file_already_in_db(database_entries, this_md5):
        print("Already in database")
        continue
    
    open_preview(this_file_path)
    is_new = get_yn("Press Y for new item, N for additional images of the last item")
    if is_new:
        this_entry = build_record_from_scratch(this_file_path)
    else:
        this_entry = build_record_from_existing(database_entries[-1], this_file_path)
    print(this_entry)
    database_entries.append(this_entry)
    save_csv(database_entries)

    # time.sleep(0.5)
    # kill_preview()
    # time.sleep(0.5)
    
