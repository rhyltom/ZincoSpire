import random



MOBS = {
    1:[
    {"name": "Rat", "hp": 20, "attack": 2},
    {"name": "Snake", "hp": 17, "attack": 3},
    {"name": "Orc", "hp": 35, "attack": 5},
    {"name": "Minotaur", "hp": 40, "attack": 5},
    ],

    2:[
        {"name": "Giant Spider", "hp": 60, "attack": 7},
    ],

    3:[
        {"name": "Giant Spider", "hp": 100, "attack": 10},
    ]
}


ELITES = {
    1: [
        {"name": "Cyclop", "hp": 55, "attack": 10},
        {"name": "Valkyrie", "hp": 70, "attack": 7},
    ],
    
    2: [
        {"name": "Giant Spider", "hp": 45, "attack": 10},
    ],

    3: [
        {"name": "Juggernaut", "hp": 45, "attack": 10},
    ]
}


BOSSES = {
    1: [
        {"name": "Dragon", "hp": 100, "attack": 15},
    ],

    2: [
        {"name": "Demon", "hp": 180, "attack": 25},
    ],

    3: [
        {"name": "Ferumbras", "hp": 180, "attack": 25},
    ]
}




def get_monster(data):

    t = data.get("type")
    act = data.get("act", 1)

    if t == "mob":
        pool = MOBS.get(act, MOBS[1])

    elif t == "elite":
        pool = ELITES.get(act, ELITES[1])

    elif t == "boss":
        act = data.get("act", 1)
        pool = BOSSES.get(act, BOSSES[1])

    else:
        print("UNKNOWN TYPE:", data)
        pool = MOBS[1]

    return random.choice(pool)