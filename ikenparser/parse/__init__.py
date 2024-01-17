import re

from .. import patterns
from .enemy import parse_enemy
from .item import parse_item

def parse_file(file):
    stripped_lines = (line.strip() for line in file.readlines())

    while (line := next(stripped_lines, None)) is not None:
        if (match := re.search(patterns.EnemyClassDefinition, line)) is not None:
            return parse_enemy(match, stripped_lines)
        elif (match := re.search(patterns.ItemClassDefinition, line)) is not None:
            item = parse_item(match, stripped_lines)
            return item

    return None
