import os
import pyjson5
from .. import config as cfg

def import_patches():
    patches = {}
    patches_dir = os.path.join(cfg.DATA_PATH, "patches")

    with os.scandir(patches_dir) as files:
        for entry in files:
            if not entry.is_file() \
                or not entry.name.endswith(".json5"):
                continue

            with open(entry.path, "r", encoding="utf-8") as file:
                patches |= pyjson5.load(file)

    return patches

def apply_patches(enemy_classes, patches):
    for enemy_class in enemy_classes:
        patch = patches.get(enemy_class.ClassName, None)
        if patch is None: continue
        for (key, value) in patch.items():
            print(f"patching {key} of {enemy_class.ClassName}")
            setattr(enemy_class, key, value)
