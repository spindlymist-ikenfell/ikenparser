def remove_abstract_classes(enemy_classes):
    enemy_classes[:] = [c for c in enemy_classes if not c.IsAbstract]

def remove_unused_fields(enemy_classes):
    for enemy_class in enemy_classes:
        del enemy_class.BaseClass
        del enemy_class.IsAbstract
        del enemy_class.NameID
        del enemy_class.GetExp
        del enemy_class.GetMoney
        del enemy_class.GetRewards
        del enemy_class.GetSteal
        del enemy_class.SpriteSet
