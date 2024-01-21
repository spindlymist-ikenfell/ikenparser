import re
from .. import patterns

def resolve_token(token, strings):
    key = token[1:]
    return strings.get(key, key)

def resolve_string(expr, strings, default=None):
    if expr is None:
        return default
    
    if '$' not in expr:
        print(f"warning: invalid string `{expr}`")
        return expr
    
    while (match := re.search(patterns.StringIDToken, expr)) is not None:
        resolved_string = resolve_token(match.group(), strings)
        expr = expr[:match.start()] + resolved_string + expr[match.end():]

    return expr

def resolve_enemy_names(enemy_classes, strings):
    for enemy_class in enemy_classes:
        enemy_class.Name = resolve_string(enemy_class.NameID, strings, enemy_class.ClassName)

def resolve_item_names(item_classes, strings):
    for item_class in item_classes:
        item_class.Name = resolve_string(item_class.NameID, strings, item_class.ClassName)

def resolve_reward_names(enemy_classes, item_map):
    for enemy_class in enemy_classes:
        for reward in enemy_class.iter_rewards():
            item_type = reward["ItemType"]
            reward["ItemName"] = item_map[item_type].Name
