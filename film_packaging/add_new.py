import os
import sys
import csv
import time
import uuid
from termcolor import colored
import psutil
import shutil
import hashlib
from PIL import Image
from shared import *

author_name_this_session = AUTHOR_NAME_MYSELF
database_entries = []

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
        return get_answer(f"What is {colored(db_key, alert_color)}? ({key_attri.notes})\n")

import subprocess

def open_preview(filepath):
    subprocess.run(["open", "-g", filepath])
    
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
    this_record[ITEM_AUTHOR_KEY] = author_name_this_session
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
    this_record[ITEM_AUTHOR_KEY] = author_name_this_session
    this_record[ITEM_TYPE_KEY] = ask_attribute(ITEM_TYPE_KEY)
    return this_record

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

this_author = get_answer("Author name this session? (Press Enter for myself)\nAdd args to reverse order\n", accept_empty=True)
if len(this_author) > 0:
    author_name_this_session = this_author

convert_keys_to_int(database_entries)
ingest_file_list = sorted(os.listdir(ingest_dir_path), reverse=len(sys.argv) > 1)

for fname in ingest_file_list:
    if not (fname.lower().endswith('.jpeg') or fname.lower().endswith('.jpg')):
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
    
    this_entry[ITEM_FILE_NAME_KEY] = make_filename_only(this_entry)
    copy_dest_path = make_filename_full_path(this_entry)

    database_entries.append(this_entry)
    save_csv(database_entries)

    shutil.copy2(this_file_path, copy_dest_path)
    
