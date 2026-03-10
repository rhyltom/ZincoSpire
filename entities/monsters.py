import random

TIER_1 = [
    {"name": "Rat", "hp": 10, "attack": 2},
    {"name": "Cave Rat", "hp": 12, "attack": 6},
    {"name": "Snake", "hp": 10, "attack": 6},
]

TIER_2 = [
    {"name": "Troll", "hp": 22, "attack": 5},
    {"name": "Orc", "hp": 28, "attack": 6},
]

TIER_3 = [
    {"name": "Orc Warrior", "hp": 40, "attack": 8},
    {"name": "Minotaur", "hp": 45, "attack": 9},
]

TIER_4 = [
    {"name": "Cyclops", "hp": 60, "attack": 12},
    {"name": "Dwarf", "hp": 55, "attack": 11},
]

BOSSES = [
    {"name": "Dragon", "hp": 120, "attack": 20},
]


def get_monster_by_difficulty(level):

    if level <= 2:
        pool = TIER_1

    elif level <= 4:
        pool = TIER_2

    elif level <= 6:
        pool = TIER_3

    elif level <= 8:
        pool = TIER_4

    else:
        pool = BOSSES

    return random.choice(pool)