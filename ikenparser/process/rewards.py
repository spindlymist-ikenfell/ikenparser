from .. import patterns
import re
from copy import deepcopy

def make_rewards(rewards_list, operator="AND"):
    return {
        "Operator": operator,
        "List": rewards_list
    }

def derive_rewards(enemy_class):
    fn = enemy_class.GetRewards

    if (match := re.search(patterns.YieldNothing, fn)) is not None:
        return make_rewards([])
    elif (match := re.search(patterns.YieldOneOrMoreItems, fn)) is not None:
        return make_rewards([
            { "ItemType": item } for item in re.findall(patterns.YieldedItemTypes, fn)
        ])
    elif (match := re.search(patterns.YieldIfGetItemCountLessThan, fn)) is not None:
        return make_rewards([{
            "ItemType": match.group(2),
            "MaxRewarded": int(match.group(1)),
            "MaxOwned": int(match.group(1)),
            "IsCombinedMax": True,
        }])
    elif (match := re.search(patterns.YieldIfShouldReward, fn)) is not None:
        return make_rewards([{
            "ItemType": match.group(3),
            "MaxRewarded": int(match.group(1)),
            "MaxOwned": int(match.group(2)),
        }])
    elif (match := re.search(patterns.YieldIfShouldRewardElseIfShouldReward, fn)) is not None:
        return make_rewards([
            {
                "ItemType": match.group(3),
                "MaxRewarded": int(match.group(1)),
                "MaxOwned": int(match.group(2)),
            },
            {
                "ItemType": match.group(6),
                "MaxRewarded": int(match.group(4)),
                "MaxOwned": int(match.group(5)),
                # "Notes": [enemy_class.addNote("only if preceding item(s) can't be acquired")],
            },
        ], "OR")
    else:
        return make_rewards([{ "ItemType": "CouldNotDerive" }])

def default_steal():
    return make_rewards([{ "ItemType": "ItemCommonCoin" }])

def derive_stealable(enemy_class):
    fn = enemy_class.GetSteal

    if (match := re.search(patterns.YieldNothing, fn)) is not None:
        return {
            "Oops": default_steal(),
            "Nice": default_steal(),
            "Great": default_steal(),
        }
    elif (match := re.search(patterns.YieldOneOrMoreItems, fn)) is not None:
        rewards_list = make_rewards([
            { "ItemType": item } for item in re.findall(patterns.YieldedItemTypes, fn)
        ])
        return {
            "Oops": rewards_list,
            "Nice": deepcopy(rewards_list),
            "Great": deepcopy(rewards_list),
        }
    elif (match := re.search(patterns.YieldIfGreatAndShouldRewardElseIfShouldReward, fn)) is not None:
        return {
            "Oops": make_rewards([
                {
                    "ItemType": match.group(6),
                    "MaxRewarded": int(match.group(4)),
                    "MaxOwned": int(match.group(5)),
                },
            ]),
            "Nice": make_rewards([
                {
                    "ItemType": match.group(6),
                    "MaxRewarded": int(match.group(4)),
                    "MaxOwned": int(match.group(5)),
                },
            ]),
            "Great": make_rewards([
                {
                    "ItemType": match.group(3),
                    "MaxRewarded": int(match.group(1)),
                    "MaxOwned": int(match.group(2)),
                },
                {
                    "ItemType": match.group(6),
                    "MaxRewarded": int(match.group(4)),
                    "MaxOwned": int(match.group(5)),
                    # "Notes": [enemy_class.addNote("only if preceding item(s) can't be acquired")],
                },
            ], "OR"),
        }
    elif (match := re.search(patterns.YieldMapItem, fn)) is not None:
        return {
            "Oops": default_steal(),
            "Nice": make_rewards([{ "ItemType": match.group(1) }]),
            "Great": make_rewards([{ "ItemType": match.group(2) }]),
        }
    elif (match := re.search(patterns.YieldMapItemWithOneMax, fn)) is not None:
        return {
            "Oops": make_rewards([{ "ItemType": match.group(1) }]),
            "Nice": make_rewards([{ "ItemType": match.group(1) }]),
            "Great": make_rewards([
                {
                    "ItemType": match.group(2),
                    "MaxRewarded": int(match.group(3)),
                    "MaxOwned": int(match.group(3)),
                },
                {
                    "ItemType": match.group(1),
                    # "Notes": [enemy_class.addNote("only if preceding item(s) can't be acquired")],
                },
            ], "OR"),
        }
    elif (match := re.search(patterns.YieldMapItemWithTwoMax, fn)) is not None:
        return {
            "Oops": make_rewards([{ "ItemType": match.group(1) }]),
            "Nice": make_rewards([{ "ItemType": match.group(1) }]),
            "Great": make_rewards([
                {
                    "ItemType": match.group(2),
                    "MaxRewarded": int(match.group(3)),
                    "MaxOwned": int(match.group(4)),
                },
                {
                    "ItemType": match.group(1),
                    # "Notes": [enemy_class.addNote("only if preceding item(s) can't be acquired")],
                },
            ], "OR"),
        }
    elif (match := re.search(patterns.StealBoth, fn)) is not None:
        return {
            "Oops": make_rewards([{ "ItemType": match.group(1) }]),
            "Nice": make_rewards([{ "ItemType": match.group(1) }]),
            "Great": make_rewards([
                { "ItemType": match.group(1) },
                { "ItemType": match.group(2) },
            ]),
        }
    elif (match := re.search(patterns.StealBothInline, fn)) is not None:
        return {
            "Oops": make_rewards([{ "ItemType": match.group(1) }]),
            "Nice": make_rewards([{ "ItemType": match.group(1) }]),
            "Great": make_rewards([
                { "ItemType": match.group(1) },
                { "ItemType": match.group(2) },
            ]),
        }
    else:
        return {
            "Oops": make_rewards([{ "ItemType": "Unknown" }]),
            "Nice": make_rewards([{ "ItemType": "Unknown" }]),
            "Great": make_rewards([{ "ItemType": "Unknown" }]),
        }

def add_sprites_to_rewards(enemy_classes, item_classes):
    for enemy_class in enemy_classes:
        for reward in enemy_class.Rewards["List"]:
            item = item_classes[reward["ItemType"]]
            reward["ItemSprite"] = item.Sprite
        for timing in enemy_class.Stealable:
            for reward in enemy_class.Stealable[timing]["List"]:
                item = item_classes[reward["ItemType"]]
                reward["ItemSprite"] = item.Sprite
