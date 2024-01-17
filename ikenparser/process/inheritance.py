from ..enemy import Enemy
from .. import config as cfg

BaseEnemyType = Enemy()
BaseEnemyType.ClassName = "EnemyType"
BaseEnemyType.IsAbstract = True
BaseEnemyType.HP = 1
BaseEnemyType.Pow = 10
BaseEnemyType.Def = 10
BaseEnemyType.Spd = 7
BaseEnemyType.Mov = 3
BaseEnemyType.Exp = 1
BaseEnemyType.Money = 0
BaseEnemyType.GetRewards = """public override IEnumerable<ItemType> GetRewards(BattleSystem system, BattleUnit unit)
{
%syield break;
}""" % (' ' * cfg.INDENT_SPACES)
BaseEnemyType.GetSteal = """public override IEnumerable<ItemType> GetSteal(BattleSystem system, HitTiming timing)
{
%syield break;
}""" % (' ' * cfg.INDENT_SPACES)

def resolve_derived_classes(enemy_classes):
    resolved_classes = { "EnemyType": BaseEnemyType, "BossType": BaseEnemyType }

    while len(resolved_classes) < len(enemy_classes) + 2:
        resolve_next_inheritance_level(enemy_classes, resolved_classes)

def resolve_next_inheritance_level(enemy_classes, resolved_classes):
    for enemy_class in enemy_classes:
        if enemy_class.ClassName in resolved_classes:
            continue

        base_class = resolved_classes.get(enemy_class.BaseClass, None)
        if base_class is None:
            continue

        if enemy_class.NameID is None:
            enemy_class.NameID = base_class.NameID
        if enemy_class.Categories is None:
            enemy_class.Categories = base_class.Categories
        if enemy_class.HP is None:
            enemy_class.HP = base_class.HP
        if enemy_class.Pow is None:
            enemy_class.Pow = base_class.Pow
        if enemy_class.Def is None:
            enemy_class.Def = base_class.Def
        if enemy_class.Spd is None:
            enemy_class.Spd = base_class.Spd
        if enemy_class.Mov is None:
            enemy_class.Mov = base_class.Mov
        if enemy_class.Exp is None:
            enemy_class.Exp = base_class.Exp
        if enemy_class.Money is None:
            enemy_class.Money = base_class.Money
        if enemy_class.GetExp is None:
            enemy_class.GetExp = base_class.GetExp
        if enemy_class.GetMoney is None:
            enemy_class.GetMoney = base_class.GetMoney
        if enemy_class.GetRewards is None:
            enemy_class.GetRewards = base_class.GetRewards
        if enemy_class.GetSteal is None:
            enemy_class.GetSteal = base_class.GetSteal
        if enemy_class.SpriteSet is None:
            enemy_class.SpriteSet = base_class.SpriteSet
        if enemy_class.Sprite is None:
            enemy_class.Sprite = base_class.Sprite
        
        resolved_classes[enemy_class.ClassName] = enemy_class
