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

for item in database_entries:
    item[ITEM_FILE_NAME_KEY] = make_filename_only(item)
    item[ITEM_AUTHOR_KEY] = AUTHOR_NAME_MYSELF

save_csv(database_entries, csv_path="new.csv")