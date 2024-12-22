import os
import sys
import csv
import time
import uuid
import psutil
import hashlib
from PIL import Image

ITEM_ID_KEY = "item_id"
DATE_ADDED_KEY = "date_added"
CHECKSUM_KEY = "md5"

no_need_to_ask_set = {ITEM_ID_KEY, DATE_ADDED_KEY, CHECKSUM_KEY}

record_key_list = [
    ITEM_ID_KEY, # same ID for the same box, can have multiple entries, such as inside, outside, and leaflet
    "item_type", # box_outside, box_inside, leaflet
    "manufacturer",
    "model", # full name, NOT including brand, including ISO, e.g. Retro 80s, Fujicolor Super HR 200
    "film_format",
    "film_speed_iso",
    "expiry_date",
    DATE_ADDED_KEY, # unix ts
    "sort_order", # smallest number shows up first
    CHECKSUM_KEY,
]

database_csv_path = "./database.csv"
ingest_dir_path = "./to_add"

if os.path.isdir(ingest_dir_path) is False:
    print(f"'{ingest_dir_path}' is not a directory.")
    exit()

db_records_list = []

try:
    csv_file = open(database_csv_path)
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        entry_list.append(row)
    # entry_list = sorted(entry_list, key=lambda x: int(x[BACKER_NUMBER_KEY]))
    csv_file.close()
except Exception as e:
    print("csv read exception:", e)

def get_md5_str(filepath):
    with open(filepath, "rb") as f:
        return hashlib.file_digest(f, "md5").hexdigest()

def is_file_already_in_db(md5_str):
    return False

def get_yn(question):
    while 1:
        response = input(f"{question}\n")
        if response.lower().startswith('y'):
            return True
        if response.lower().startswith('n'):
            return False

def get_answer(question):
    while 1:
        response = input(f"{question}")
        response = response.strip()
        if len(response) > 1:
            return response

def open_preview(filepath):
    os.system(f"open {filepath}")

def kill_preview():
    for proc in psutil.process_iter():
        if proc.name() == "Preview":
            proc.kill()

def get_empty_record():
    this_dict = {}
    for key in record_key_list:
        this_dict[key] = None
    return this_dict

def build_record_from_scratch(filepath):
    this_record = get_empty_record()
    this_record[ITEM_ID_KEY] = uuid.uuid4().hex
    this_record[DATE_ADDED_KEY] = int(time.time())
    this_record[CHECKSUM_KEY] = get_md5_str(filepath)

    for key in this_record:
        if key in no_need_to_ask_set:
            continue
        this_record[key] = get_answer(f"What is {key}?\n")

    return this_record

ingest_file_list = sorted(os.listdir(ingest_dir_path))
for fname in ingest_file_list:
    if fname.lower().endswith('.jpeg') is False:
        continue
    this_file_path = os.path.join(ingest_dir_path, fname)
    this_md5 = get_md5_str(this_file_path)
    print(f"Processing {fname}...")
    if is_file_already_in_db(this_md5):
        print("Already in database")
        continue
    
    open_preview(this_file_path)

    this_entry = build_record_from_scratch(this_file_path)
    print(this_entry)

    exit()

    # open_preview(this_file_path)
    # time.sleep(2)
    # kill_preview()
    
