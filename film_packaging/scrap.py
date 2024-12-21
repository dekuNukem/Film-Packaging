import os
import sys
import csv
import time
import psutil
import hashlib
from PIL import Image

record_key_dict = {
    "film_speed":None,
    "item_type":["film_box_outside", "film_box_inside", "film_box_instruction_leaflet"],
    "expiry_date":None,
    "manufacturer":None,
    "model_name_full":None, # NOT including brand, including ISO, e.g. Retro 80s, Fujicolor Super HR 200
    "film_size":["120", "35mm", "APS"],
    "date_added":None, # unix ts,
    "item_id":None, # same ID for the same box, can have multiple entries, such as inside, outside, and leaflet
    "sort_order":None, # smallest number shows up first
    "img_checksum":None,
}

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

def open_preview(filepath):
    os.system(f"open {filepath}")

def kill_preview():
    for proc in psutil.process_iter():
        if proc.name() == "Preview":
            proc.kill()

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
    time.sleep(2)
    kill_preview()
    






