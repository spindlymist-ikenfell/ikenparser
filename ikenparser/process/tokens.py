def add_search_tokens(enemy_classes):
    for enemy in enemy_classes:
        name_tokens = set()
        add_tokens_to_set(enemy.Name, name_tokens)
        add_tokens_to_set(enemy.ClassName, name_tokens)

        reward_tokens = set()
        for reward in enemy.iter_rewards():
            add_tokens_to_set(reward["ItemName"], reward_tokens)
        
        enemy.NameTokens = list(name_tokens)
        enemy.RewardTokens = list(reward_tokens)

def add_tokens_to_set(the_string, the_set):
    parts = the_string.split(' ')
    for i in range(len(parts)):
        the_set.add(parts[i])
        the_set.add(' '.join(parts[i:]))
