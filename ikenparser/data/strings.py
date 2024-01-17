import os
import csv
from .. import config as cfg

def parse_csv(file, strings):
    reader = csv.DictReader(file)
    for row in reader:
        id = row["id"]
        name = row["en-US"]
        if len(id) > 0 and len(name) > 0:
            strings[id] = name

def import_strings():
    strings = {}
    strings_dir = os.path.join(cfg.DATA_PATH, "strings")

    with os.scandir(strings_dir) as files:
        for entry in files:
            if not entry.is_file() \
                or not entry.name.endswith(".csv"):
                continue

            with open(entry.path, "r", newline="", encoding="utf-8") as csv:
                parse_csv(csv, strings)

    return strings
