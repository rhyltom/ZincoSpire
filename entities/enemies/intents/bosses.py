import random

def dragon_lord_intent(state):
    pattern = [
        {"type": "attack", "value": state.enemy_attack},
        {"type": "burn", "value": 3},
        {"type": "buff"},
    ]
    return pattern[state.enemy_timer % len(pattern)]


def hydra_intent(state):
    if state.enemy_timer % 2 == 0:
        return {"type": "attack_multi", "value": 3}
    else:
        return {"type": "heal", "value": 5}


def behemoth_intent(state):
    if state.enemy_timer % 2 == 0:
        return {"type": "buff"}
    else:
        return {"type": "attack", "value": state.enemy_attack + 8}