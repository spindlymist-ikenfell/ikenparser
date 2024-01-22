import re

def fn_regex(body_pattern):
    return re.compile(r'^.+\s+{\s+' + body_pattern + r'\s+}$')

EnemyTypes = [
    "BossType",
    "EnemyType",
    "EnemyAllcatCat",
    "EnemyAutochopper",
    "EnemyBee",
    "EnemyBlueBird",
    "EnemyBook",
    "EnemyBookPurple",
    "EnemyBunwitch",
    "EnemyButterfly",
    "EnemyCrackedGhost",
    "EnemyDarkeye",
    "EnemyEyeFlower",
    "EnemyFakeTile",
    "EnemyFungi",
    "EnemyFuzzy",
    "EnemyGhrostling",
    "EnemyJelly",
    "EnemyLamp",
    "EnemyLanternFlame",
    "EnemyPaneAttacker",
    "EnemyPants",
    "EnemyRedBird",
    "EnemySackboy",
    "EnemySackpole",
    "EnemySnatcherPants",
    "EnemySpec",
    "EnemySpelltile",
    "EnemySpychopper",
    "EnemyTinyStar",
]

ItemTypes = [
    "ItemType",
    "KeyItemType",

    # Consumables
    "ConsumableType",
    "HPHealingItem",
    "StatBuffItem",
    "ItemHealStatus",

    # Equipment
    "EquipmentType",
    "AccessoryType",
    "ArmorType",
    "BootsType",
    "HatType",
    "WeaponType",
]

StringIDToken = re.compile(r'\$([a-z0-9_])*')
SpriteName = r'(?P<SpriteName>(?P<SpriteSet>[^"]+)_(\d)+_(\d)+)'

EnemyClassDefinition = re.compile(r'^public( abstract)? class (Enemy\w+) : (' + '|'.join(EnemyTypes) + r')$')
EnemyInitMethodDefinition = re.compile(r'^public override void Init\(\)$')
GetStealMethodDefinition = re.compile(r'^(public override IEnumerable<ItemType> GetSteal\(BattleSystem system, HitTiming timing\))$')
GetRewardsMethodDefinition = re.compile(r'^(public override IEnumerable<ItemType> GetRewards\(BattleSystem system, BattleUnit unit\))$')

ItemClassDefinition = re.compile(r'^public class (\w+) : (' + '|'.join(ItemTypes) + r')$')
ItemInitializerList = re.compile(r'^: base\("([^"]+)", "' + SpriteName + r'".*\)$')

SetNameID = re.compile(r'^base\.NameID = "([^"]*)";$')         # base.NameID = "$aeldra_name";
SetCategory = re.compile(r'^base\.Category = ')                # base.Category = UnitCategory.Flying | UnitCategory.Human;
CategoryNames = re.compile(r'UnitCategory\.(\w+)')
SetHP = re.compile(r'^SetBaseStat\(UnitStat\.HP, (\d+)\);$')   # SetBaseStat(UnitStat.HP, 500);
SetPow = re.compile(r'^SetBaseStat\(UnitStat\.Pow, (\d+)\);$') # SetBaseStat(UnitStat.Pow, 58);
SetDef = re.compile(r'^SetBaseStat\(UnitStat\.Def, (\d+)\);$') # SetBaseStat(UnitStat.Def, 110);
SetSpd = re.compile(r'^SetBaseStat\(UnitStat\.Spd, (\d+)\);$') # SetBaseStat(UnitStat.Spd, 80);
SetMov = re.compile(r'^SetBaseStat\(UnitStat\.Mov, (\d+)\);$') # SetBaseStat(UnitStat.Mov, 4);
SetExp = re.compile(r'^base\.Exp = (\d+);$')                   # base.Exp = 0;
SetMoney = re.compile(r'^base\.Money = (\d+);$')               # base.Money = 0;
SetSprite = re.compile(r'^base\.Anims\.Sprite = Assets\.GetSprite\("' + SpriteName + r'"\);$') # base.Anims.Sprite = Assets.GetSprite("battle_aeldra_0_0");

GetExpLambda = re.compile(r'^GetExpFunc = (\(BattleSystem sys\) => (.+);)$')     # GetExpFunc = (BattleSystem sys) => ...;
GetExpDelegate = re.compile(r'^GetExpFunc = (delegate\(BattleSystem sys\))$')    # GetExpFunc = delegate(BattleSystem sys)
GetMoneyLambda = re.compile(r'^GetMoneyFunc = (\(BattleSystem sys\) => (.+);)$') # GetExpFunc = (BattleSystem sys) => ...;
NoExpOrMoney = re.compile(r'^NoExpOrMoney\(\);$')

YieldNothing = fn_regex(r'yield break;')
YieldOneOrMoreItems = fn_regex(r'(\s*yield return Items\.Get<\w+>\(\);)+')
YieldedItemTypes = re.compile(r'Items.Get<(\w+)>\(\);')
YieldIfGetItemCountLessThan = fn_regex(\
    r'if \(system\.GetItemCount<\w+>\(\) < (\d+)\)\s+{\s+yield return Items\.Get<(\w+)>\(\);\s+}')
YieldIfShouldReward = fn_regex(\
    r'if \(system\.ShouldReward<\w+>\((\d+), (\d+)\)\)\s+' +\
    r'{\s+' +\
    r'yield return Items\.Get<(\w+)>\(\);\s+' +\
    r'}'
)
YieldIfShouldRewardElseIfShouldReward = fn_regex(\
    r'if \(system\.ShouldReward<\w+>\((\d+), (\d+)\)\)\s+' +\
    r'{\s+' +\
    r'yield return Items\.Get<(\w+)>\(\);\s+' +\
    r'}\s+' +\
    r'else if \(system\.ShouldReward<\w+>\((\d+), (\d+)\)\)\s+' +\
    r'{\s+' +\
    r'yield return Items\.Get<(\w+)>\(\);\s+' +\
    r'}'
)
YieldIfGreatAndShouldRewardElseIfShouldReward = fn_regex(\
    r'if \(timing == HitTiming\.Great && system\.ShouldReward<\w+>\((\d+), (\d+)\)\)\s+' +\
    r'{\s+' +\
    r'yield return Items\.Get<(\w+)>\(\);\s+' +\
    r'}\s+' +\
    r'else if \(system\.ShouldReward<\w+>\((\d+), (\d+)\)\)\s+' +\
    r'{\s+' +\
    r'yield return Items\.Get<(\w+)>\(\);\s+' +\
    r'}'
)
YieldMapItem = fn_regex(r'yield return timing\.MapItem<(\w+), (\w+)>\(\);')
YieldMapItemWithOneMax = fn_regex(r'yield return timing\.MapItem<(\w+), (\w+)>\(system, (\d+)\);')
YieldMapItemWithTwoMax = fn_regex(r'yield return timing\.MapItem<(\w+), (\w+)>\(system, (\d+), (\d+)\);')
StealBoth = fn_regex(r'return timing\.StealBoth<(\w+), (\w+)>\(\);')
StealBothInline = fn_regex(\
    r'yield return Items\.Get<(\w+)>\(\);\s+' +\
    r'if \(timing == HitTiming\.Great\)\s+' +\
    r'{\s+' +\
    r'yield return Items\.Get<(\w+)>\(\);\s+' +\
    r'}'
)