import re

from .. import patterns
from ..item import Item

def parse_item(match, lines):
    item = Item()
    item.ClassName = match.group(1)

    while (line := next(lines, None)) is not None:
        if (match := re.search(patterns.ItemInitializerList, line)) is not None:
            item.NameID = match.group(1)
            item.Sprite = match.group("SpriteID")
            item.SpriteSet = match.group("SpriteSet")
            break

    return item
