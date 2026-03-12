from ui.damage_text import DamageText


def shield_block(combat):
    block = 8
    combat.player.block += block
    combat.damage_texts.append(
        DamageText(400, 330, str(block), (120,200,255))
    )
    combat.player_turn = False



def mana_shield(combat):
    cost = 2
    if combat.player.mana < cost:
        return
    combat.player.mana -= cost
    block = 6
    combat.player.block += block
    combat.damage_texts.append(
        DamageText(400, 330, str(block), (120,200,255))
    )
    combat.player_turn = False



def evade(combat):
    combat.player.evade = True
    combat.damage_texts.append(
        DamageText(400, 330, "Evade", (200,200,200))
    )
    combat.player_turn = False



def fireball(combat):
    cost = 2
    if combat.player.mana < cost:
        return
    combat.player.mana -= cost
    damage = combat.player.mgc * 3
    combat.enemy_hp -= damage
    combat.damage_texts.append(
        DamageText(400,110,str(damage),(80,120,255))
    )
    combat.hit_flash = 6
    combat.shake = 6
    combat.player_turn = False



def power_strike(combat):
    damage = (combat.player.attack + combat.player.str) * 2
    combat.enemy_hp -= damage
    combat.damage_texts.append(
        DamageText(400,110,str(damage),(255,80,80))
    )
    combat.hit_flash = 6
    combat.shake = 6
    combat.player_turn = False



def power_shot(combat):
    damage = int((combat.player.attack + combat.player.str) * 1.5)
    combat.enemy_hp -= damage
    combat.damage_texts.append(
        DamageText(400,110,str(damage),(255,200,80))
    )
    combat.hit_flash = 6
    combat.shake = 6
    combat.player_turn = False