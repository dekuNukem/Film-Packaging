import os
import sys
import csv
import time
import psutil
import hashlib
from PIL import Image

record_key_list = [
    "film_speed",
    "item_type",
    "expiry_date",
    "manufacturer",
    "model_name_full",
    "film_size",
    "date_added",
    "item_id",
    "sort_order",
    "img_checksum",
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

def open_preview(filepath):
    os.system(f"open {filepath}")

def kill_preview():
    for proc in psutil.process_iter():
        if proc.name() == "Preview":
            proc.kill()


