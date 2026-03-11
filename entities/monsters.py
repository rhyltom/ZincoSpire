import random

TIER_1 = [
    {"name": "Rat", "hp": 10, "attack": 2},
    {"name": "Cave Rat", "hp": 12, "attack": 2},
    {"name": "Snake", "hp": 10, "attack": 3},
]

TIER_2 = [
    {"name": "Orc", "hp": 25, "attack": 6},
    {"name": "Minotaur", "hp": 30, "attack": 5},
]

TIER_3 = [
]

TIER_4 = [
    {"name": "Dwarf", "hp": 55, "attack": 11},
]

BOSSES = [
    {"name": "Dragon", "hp": 120, "attack": 20},
]


def get_monster_by_difficulty(tier):

    if tier == 1:
        pool = TIER_1

    elif tier == 2:
        pool = TIER_2

    elif tier == 3:
        pool = TIER_3

    elif tier == 4:
        pool = TIER_4

    else:
        pool = BOSSES

    return random.choice(pool)