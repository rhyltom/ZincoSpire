from ui.damage_text import DamageText


# ========================
# HELPERS
def apply_magic_bonus(combat, damage):
    if combat.player.passive["name"] == "Arcane Power":
        return int(damage * 1.2)
    return damage


# ========================
# DEFENSIVE SKILLS
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


# ========================
# WARRIOR SKILLS
def power_strike(combat):

    damage = (combat.player.attack + combat.player.str + combat.temp_str) * 2

    combat.enemy_hp -= damage

    combat.damage_texts.append(
        DamageText(400,110,str(damage),(255,80,80))
    )

    combat.enemy_bleed += 2
    combat.damage_texts.append(
        DamageText(400,140,"Bleeding!",(255,120,0))
    )

    combat.hit_flash = 6
    combat.shake = 6

    combat.player_turn = False


def whirlwind(combat):

    damage = int((combat.player.attack + combat.player.str + combat.temp_str) * 1.3)

    combat.enemy_hp -= damage

    combat.damage_texts.append(
        DamageText(400,110,str(damage),(255,120,80))
    )

    combat.hit_flash = 6
    combat.shake = 6

    combat.player_turn = False


def berserk(combat):

    buff = 2
    combat.temp_str += buff

    combat.damage_texts.append(
        DamageText(400,330,f"+{buff} STR",(255,50,50))
    )

    combat.player_turn = False


# ========================
# MAGE SKILLS
def fireball(combat):
    cost = 2

    if combat.player.mana < cost:
        return

    combat.player.mana -= cost
    damage = combat.player.mgc * 3
    damage = apply_magic_bonus(combat, damage)
    combat.enemy_hp -= damage
    combat.damage_texts.append(
        DamageText(400,110,str(damage),(80,120,255))
    )

    combat.enemy_burn += 2
    combat.damage_texts.append(
        DamageText(400,140,"Burn!",(255,120,0))
    )

    combat.hit_flash = 6
    combat.shake = 6
    combat.player_turn = False




def ice_blast(combat):

    cost = 2

    if combat.player.mana < cost:
        return

    combat.player.mana -= cost

    damage = int(combat.player.mgc * 2.5)
    damage = apply_magic_bonus(combat, damage)

    combat.enemy_hp -= damage

    combat.damage_texts.append(
        DamageText(400,110,str(damage),(150,200,255))
    )

    combat.hit_flash = 6
    combat.shake = 6

    combat.player_turn = False


def lightning(combat):

    cost = 3

    if combat.player.mana < cost:
        return

    combat.player.mana -= cost

    damage = int(combat.player.mgc * 4)
    damage = apply_magic_bonus(combat, damage)

    combat.enemy_hp -= damage

    combat.damage_texts.append(
        DamageText(400,110,str(damage),(255,255,100))
    )

    combat.hit_flash = 6
    combat.shake = 6

    combat.player_turn = False


# ========================
# HUNTER SKILLS

def flaming_arrow(combat):

    damage = int((combat.player.attack + combat.player.str + combat.temp_str) * 1.2)
    combat.enemy_hp -= damage

    combat.damage_texts.append(
        DamageText(400,110,str(damage),(255,150,50))
    )
    combat.enemy_burn += 2

    combat.damage_texts.append(
        DamageText(400,140,"Burn!",(255,120,0))
    )
    combat.hit_flash = 6
    combat.shake = 6
    combat.player_turn = False



def poison_arrow(combat):

    damage = int((combat.player.attack + combat.player.str + combat.temp_str) * 1.2)
    combat.enemy_hp -= damage

    combat.damage_texts.append(
        DamageText(400,110,str(damage),(100,255,100))
    )
    combat.enemy_poison += 3
    combat.hit_flash = 6
    combat.shake = 6
    combat.player_turn = False



def rapid_fire(combat):

    damage = int(combat.player.attack * 0.8)
    total = damage * 2

    combat.enemy_hp -= total

    combat.damage_texts.append(
        DamageText(400,110,str(total),(255,180,80))
    )

    combat.hit_flash = 6
    combat.shake = 6

    combat.player_turn = False