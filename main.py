import json
import os

from ikenparser.enemy import Enemy
from ikenparser.item import Item
from ikenparser.parse import parse_file
from ikenparser.process.inheritance import resolve_derived_classes
from ikenparser.process.resolve_strings import resolve_enemy_names, resolve_item_names, resolve_reward_names
from ikenparser.process.rewards import derive_rewards, derive_stealable, add_sprites_to_rewards
from ikenparser.process.cleanup import remove_unused_fields, remove_abstract_classes
from ikenparser.data.strings import import_strings
from ikenparser.data.patches import import_patches, apply_patches
from ikenparser.data.sprites import copy_sprites_to
import ikenparser.config as cfg

# cfg.DEBUG = True

if __name__ == "__main__":
    enemy_classes = []
    item_classes = {}

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
                    item_classes[result.ClassName] = result

    resolve_derived_classes(enemy_classes)

    for enemy_class in enemy_classes:
        enemy_class.Rewards = derive_rewards(enemy_class)
        enemy_class.Stealable = derive_stealable(enemy_class)

    patches = import_patches()
    apply_patches(enemy_classes, patches)

    strings = import_strings()
    resolve_enemy_names(enemy_classes, strings)
    resolve_item_names(item_classes, strings)
    resolve_reward_names(enemy_classes, item_classes)

    add_sprites_to_rewards(enemy_classes, item_classes)
    # copy_sprites_to("../ikenfell-bestiary/public/images/sprites", enemy_classes, item_classes)

    if not cfg.DEBUG:
        remove_abstract_classes(enemy_classes)
        remove_unused_fields(enemy_classes)

    with open("./enemies.json", "w") as file:
        json.dump(enemy_classes, file, default=vars, indent=4)
