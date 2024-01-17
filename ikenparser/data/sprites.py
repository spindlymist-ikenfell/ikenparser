import os, shutil
from itertools import chain
from .. import config as cfg

def copy_sprites_to(output_dir, enemy_classes, item_classes):
    sprites_dir = os.path.join(cfg.DATA_PATH, "sprites")
    to_copy = set()

    for sprite_class in chain(enemy_classes, item_classes.values()):
        if (sprite_class.Sprite is None):
            print (sprite_class.ClassName, "no sprite")
        else:
            to_copy.add((sprite_class.SpriteSet, sprite_class.Sprite))
    
    for (sprite_set, sprite) in to_copy:
        filename = f"{sprite}.png"
        from_path = os.path.join(sprites_dir, sprite_set, filename)
        shutil.copy(from_path, output_dir)
