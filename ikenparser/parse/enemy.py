import re

from ..enemy import Enemy
from .. import patterns
from .common import consume_matched_braces

def parse_enemy(match, lines):
    enemy = Enemy()
    enemy.IsAbstract = match.group(1) is not None
    enemy.ClassName = match.group(2)
    enemy.BaseClass = match.group(3)

    while (line := next(lines, None)) is not None:
        if (match := re.search(patterns.EnemyInitMethodDefinition, line)) is not None:
            parse_Init_method(match, lines, enemy)
        elif (match := re.search(patterns.GetRewardsMethodDefinition, line)) is not None:
            enemy.GetRewards = parse_GetRewards_method(match, lines)
        elif (match := re.search(patterns.GetStealMethodDefinition, line)) is not None:
            enemy.GetSteal = parse_GetSteal_method(match, lines)

    return enemy

def parse_Init_method(match, lines, enemy):
    brace_count = 0

    while (line := next(lines, None)) is not None:
        if (match := re.search(patterns.SetNameID, line)) is not None:
            enemy.NameID = match.group(1)
        elif (match := re.search(patterns.SetCategory, line)) is not None:
            enemy.Categories = re.findall(patterns.CategoryNames, line)
        elif (match := re.search(patterns.SetHP, line)) is not None:
            enemy.HP = int(match.group(1))
        elif (match := re.search(patterns.SetPow, line)) is not None:
            enemy.Pow = int(match.group(1))
        elif (match := re.search(patterns.SetDef, line)) is not None:
            enemy.Def = int(match.group(1))
        elif (match := re.search(patterns.SetSpd, line)) is not None:
            enemy.Spd = int(match.group(1))
        elif (match := re.search(patterns.SetMov, line)) is not None:
            enemy.Mov = int(match.group(1))
        elif (match := re.search(patterns.SetExp, line)) is not None:
            enemy.Exp = int(match.group(1))
        elif (match := re.search(patterns.SetMoney, line)) is not None:
            enemy.Money = int(match.group(1))
        elif (match := re.search(patterns.GetExpLambda, line)) is not None:
            enemy.GetExp = match.group(1)
        elif (match := re.search(patterns.GetExpDelegate, line)) is not None:
            enemy.GetExp = parse_GetExpFunc_delegate(match, lines)
        elif (match := re.search(patterns.GetMoneyLambda, line)) is not None:
            enemy.GetMoney = match.group(1)
        elif (match := re.search(patterns.NoExpOrMoney, line)) is not None:
            enemy.Exp = 0
            enemy.Money = 0
        elif (match := re.search(patterns.SetSprite, line)) is not None:
            enemy.Sprite = match.group("SpriteID")
            enemy.SpriteSet = match.group("SpriteSet")
        elif line == "{":
            brace_count += 1
        elif line.startswith("}"):
            brace_count -= 1    
            if brace_count == 0:
                break
    
    if enemy.Categories is None:
        enemy.Categories = []

def parse_GetExpFunc_delegate(match, lines):
    return consume_matched_braces(match.group(1), lines)

def parse_GetRewards_method(match, lines):
    return consume_matched_braces(match.group(1), lines)

def parse_GetSteal_method(match, lines):
    return consume_matched_braces(match.group(1), lines)
