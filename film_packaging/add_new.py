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

author_name_this_session = "Unknown"
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

def format_two_columns(items):
    MAX_COL_WIDTH = 50
    col_width = min(max((len(f"{i}:  {item}") for i, item in enumerate(items)), default=0) + 4, MAX_COL_WIDTH)
    half = (len(items) + 1) // 2
    lines = []
    for row in range(half):
        left_i = row
        left = f"{left_i}:  {items[left_i]}"
        right_i = row + half
        if right_i < len(items):
            right = f"{right_i}:  {items[right_i]}"
            lines.append(f"{left:<{col_width}}{right}")
        else:
            lines.append(left)
    return "\n".join(lines) + "\n"

def ask_with_listing_existing_options(db_key):
    all_options = set()
    for item in database_entries:
        if len(str(item[db_key])) > 0:
            all_options.add(item[db_key])
    all_options = sorted([str(x) for x in all_options])
    option_list_str = format_two_columns(all_options)
    question_to_ask = f"\nWhat is {colored(db_key, alert_color)}?\nSelect existing option or type a new entry\n{option_list_str}"
    user_answer = get_answer(question_to_ask)
    try:
        return all_options[int(user_answer)]
    except Exception as e:
        # print("ask_with_listing_existing_options:", e)
        pass
    return user_answer

NON_NUMERIC_QUANTITY_LIST = ["N/A", "Unknown"]

def ask_quantity():
    while True:
        user_answer = ask_with_listing_existing_options(ITEM_QUANTITY_KEY)
        if is_number(user_answer) or user_answer in NON_NUMERIC_QUANTITY_LIST:
            return user_answer
        print(colored(f"Quantity must be a number (unit is asked next), or one of {NON_NUMERIC_QUANTITY_LIST}", alert_color))

def ask_attribute(db_key):
    key_attri = find_key_attributes(db_key)
    if key_attri.no_need_to_ask:
        return
    if db_key == ITEM_QUANTITY_KEY:
        return ask_quantity()
    if key_attri.list_existing:
        return ask_with_listing_existing_options(db_key)
    else:
        return get_answer(f"What is {colored(db_key, alert_color)}? ({key_attri.notes})\n", accept_empty=key_attri.accept_empty)

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
        if keyname == ITEM_UNIT_KEY and is_number(this_record[ITEM_QUANTITY_KEY]) is False:
            this_record[keyname] = ''
            continue
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

def find_entry_by_uuid(entries, uuid_str):
    for item in entries:
        if str(item[ITEM_UUID_KEY]) == uuid_str:
            return item
    return None

def get_next_subindex(item_index):
    max_sub = -1
    for item in database_entries:
        if int(item[ITEM_INDEX_KEY]) == int(item_index):
            max_sub = max(max_sub, int(item[ITEM_SUBINDEX_KEY]))
    return max_sub + 1

def build_record_from_existing(template, filepath, use_session_author=True):
    this_record = get_empty_record()
    for key in this_record:
        this_record[key] = template[key]
    this_record[ITEM_INDEX_KEY] = template[ITEM_INDEX_KEY]
    this_record[DATE_ADDED_KEY] = int(time.time())
    this_record[CHECKSUM_KEY] = get_md5_str(filepath)
    this_record[ITEM_UUID_KEY] = uuid.uuid4().hex
    this_record[ITEM_SUBINDEX_KEY] = get_next_subindex(template[ITEM_INDEX_KEY])
    if use_session_author:
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

did_resize = get_answer(f"Have you run the resize script?", accept_empty=True)

author_prompted = False

def ensure_author_name():
    global author_name_this_session, author_prompted
    if author_prompted:
        return
    author_prompted = True
    latest_author = database_entries[-1][ITEM_AUTHOR_KEY]
    all_authors = sorted(set(item[ITEM_AUTHOR_KEY] for item in database_entries))
    author_list_str = format_two_columns(all_authors)
    user_answer = get_answer(
        f"Author name this session? (Press Enter for {latest_author})\n{author_list_str}",
        accept_empty=True
    )
    if len(user_answer) == 0:
        author_name_this_session = latest_author
    else:
        try:
            author_name_this_session = all_authors[int(user_answer)]
        except (ValueError, IndexError):
            author_name_this_session = user_answer

convert_keys_to_int(database_entries)
ingest_file_list = sorted(os.listdir(ingest_dir_path), reverse=len(sys.argv) > 1)

for item in ingest_file_list:
    print(item)

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
    while True:
        choice = get_answer(
            "Press Y for new item\n"
            "Press N for additional images of the last item\n"
            "Press U to add additional images to an existing entry by UUID\n"
        ).lower()
        if choice.startswith('y') or choice.startswith('n') or choice.startswith('u'):
            break
        print(colored("Invalid choice, please try again.", alert_color))

    if choice.startswith('y'):
        ensure_author_name()
        this_entry = build_record_from_scratch(this_file_path)
    elif choice.startswith('u'):
        target_uuid = get_answer("Enter the UUID of the existing entry: ").strip()
        template = find_entry_by_uuid(database_entries, target_uuid)
        if template is None:
            print(colored(f"UUID '{target_uuid}' does not exist in the database.", alert_color))
            kill_preview()
            exit()
        this_entry = build_record_from_existing(template, this_file_path, use_session_author=False)
    else:
        ensure_author_name()
        this_entry = build_record_from_existing(database_entries[-1], this_file_path)
    
    this_entry[ITEM_FILE_NAME_KEY] = make_filename_only(this_entry)
    copy_dest_path = make_filename_full_path(this_entry)

    database_entries.append(this_entry)
    database_entries.sort(key=lambda e: (int(e[ITEM_INDEX_KEY]), int(e[ITEM_SUBINDEX_KEY])))
    save_csv(database_entries)

    shutil.copy2(this_file_path, copy_dest_path)
    
