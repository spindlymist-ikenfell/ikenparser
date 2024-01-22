import os, shutil
from itertools import chain
from PIL import Image

from ..sprite import Sprite
from .. import config as cfg

def resolve_sprites(classes):
    sprites_dir = os.path.join(cfg.DATA_PATH, "sprites")
    sprite_map = {}

    max_width = 0
    max_height = 0

    for class_ in classes:
        if class_.Sprite is None:
            print(f"warning: no sprite for `{class_.ClassName}`")
            continue

        if (sprite := sprite_map.get(class_.Sprite, None)) is not None:
            class_.Sprite = sprite
            continue

        sprite = Sprite(class_.Sprite, class_.SpriteSet)

        path = os.path.join(sprites_dir, sprite.Set, f"{sprite.Name}.png")
        with Image.open(path) as image:
            sprite.Width = image.size[0]
            sprite.Height = image.size[1]

        max_width = max(max_width, sprite.Width)
        max_height = max(max_height, sprite.Height)

        class_.Sprite = sprite
        sprite_map[sprite.Name] = sprite
    
    return (sprite_map, max_width, max_height)

def copy_sprites(sprites):
    sprites_dir = os.path.join(cfg.DATA_PATH, "sprites")
    output_dir = os.path.join(cfg.OUTPUT_PATH, "sprites")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    for sprite in sprites:
        from_path = os.path.join(sprites_dir, sprite.Set, f"{sprite.Name}.png")
        shutil.copy(from_path, output_dir)

def copy_and_resize_sprites(sprites, width=None, height=None):
    sprites_dir = os.path.join(cfg.DATA_PATH, "sprites")
    output_dir = os.path.join(cfg.OUTPUT_PATH, "sprites")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    for sprite in sprites:
        filename = f"{sprite.Name}.png"
        from_path = os.path.join(sprites_dir, sprite.Set, filename)
        to_path = os.path.join(output_dir, filename)

        with Image.open(from_path) as image_in:
            image_out = Image.new(
                "RGBA",
                (width or image_in.size[0], height or image_in.size[1]),
                (0, 0, 0, 0),
            )

            x = (image_out.size[0] - image_in.size[0]) // 2
            y = (image_out.size[1] - image_in.size[1]) // 2

            image_out.paste(image_in, (x, y))
            image_out.save(to_path)

            sprite.Width = image_out.size[0]
            sprite.Height = image_out.size[1]
