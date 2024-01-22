import json
import os
import shutil

from ikenparser.enemy import Enemy
from ikenparser.item import Item
from ikenparser.parse import parse_file
from ikenparser.process.inheritance import resolve_derived_classes
from ikenparser.process.resolve_strings import resolve_enemy_names, resolve_item_names, resolve_reward_names
from ikenparser.process.rewards import derive_rewards, derive_stealable, add_sprites_to_rewards
from ikenparser.process.cleanup import remove_unused_fields, remove_abstract_classes, filter_unused_items
from ikenparser.data.strings import import_strings
from ikenparser.data.patches import import_patches, apply_patches
from ikenparser.data.sprites import resolve_sprites, copy_sprites, copy_and_resize_sprites
import ikenparser.config as cfg

# cfg.DEBUG = True

def main():
    if os.path.exists(cfg.OUTPUT_PATH):
        if os.path.isdir(cfg.OUTPUT_PATH):
            confirm = input(f"delete `{cfg.OUTPUT_PATH}` [y/n]? ")
            if confirm != "y" and confirm != "yes":
                return
            shutil.rmtree(cfg.OUTPUT_PATH)
        else:
            print("error: can't create output directory")
            return
    
    os.makedirs(cfg.OUTPUT_PATH)

    enemy_classes = []
    item_map = {}

    with os.scandir("./csharp/LittleWitch") as files:
        for entry in files:
            if (
                not entry.is_file()
                or not entry.name.endswith(".cs")
            ):
                continue

            with open(entry.path, "r", encoding="utf-8") as file:
                result = parse_file(file)
                if isinstance(result, Enemy):
                    enemy_classes.append(result)
                elif isinstance(result, Item):
                    item_map[result.ClassName] = result

    resolve_derived_classes(enemy_classes)

    for enemy_class in enemy_classes:
        enemy_class.Rewards = derive_rewards(enemy_class)
        enemy_class.Stealable = derive_stealable(enemy_class)

    patches = import_patches()
    apply_patches(enemy_classes, patches)

    item_classes = filter_unused_items(enemy_classes, item_map)

    strings = import_strings()
    resolve_enemy_names(enemy_classes, strings)
    resolve_item_names(item_classes, strings)
    resolve_reward_names(enemy_classes, item_map)

    (enemy_sprite_map, __, __) = resolve_sprites(enemy_classes)
    (item_sprite_map, item_max_width, item_max_height) = resolve_sprites(item_classes)

    add_sprites_to_rewards(enemy_classes, item_map)
    copy_sprites(enemy_sprite_map.values())
    copy_and_resize_sprites(item_sprite_map.values(), item_max_width)

    if not cfg.DEBUG:
        remove_abstract_classes(enemy_classes)
        remove_unused_fields(enemy_classes)

    with open(os.path.join(cfg.OUTPUT_PATH, "enemies.json"), "w") as file:
        json.dump(enemy_classes, file, default=vars, indent=4)

if __name__ == "__main__":
    main()
