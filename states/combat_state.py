import pygame
import random

from ui.damage_text import DamageText
from ui.button import Button
from entities.monsters import get_monster

# Import das skills
from skills.skills import (
    fireball,
    power_strike,
    flaming_arrow,
    shield_block,
    mana_shield,
    evade,
    whirlwind,
    berserk,
    ice_blast,
    lightning,
    poison_arrow,
    rapid_fire,
)

from entities.enemies.intents.bosses import (
    dragon_lord_intent,
    hydra_intent,
    behemoth_intent,
)

# ========================
# CONSTANTES DE UI
# ========================
SCREEN_WIDTH = 1000
PANEL_WIDTH = 280

COMBAT_WIDTH = SCREEN_WIDTH - PANEL_WIDTH
COMBAT_CENTER_X = COMBAT_WIDTH // 2

ENEMY_Y = 140

PLAYER_HP_Y = 350
PLAYER_LABEL_Y = 320

TURN_TEXT_Y = 410
BUTTON_Y = 440

MAX_SKILLS = 3


# ========================
# DESENHAR BARRA DE VIDA
# ========================
def draw_hp_bar(screen, x, y, width, height, current_hp, max_hp, font):
    ratio = current_hp / max_hp

    pygame.draw.rect(screen, (120,0,0), (x, y, width, height))          # fundo (vermelho escuro)
    pygame.draw.rect(screen, (0,200,0), (x, y, width * ratio, height))   # vida atual
    pygame.draw.rect(screen, (255,255,255), (x, y, width, height), 2)    # border

    # HP points
    hp_text = font.render(f"{current_hp}/{max_hp}", True, (255,255,255))
    text_rect = hp_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(hp_text, text_rect)


class CombatState:

    # ========================
        # APLICA MODIFICADORES AO DANO
    # ========================
    def deal_damage(self, damage):

        # Se inimigo tiver bleed, leva mais dano (vulnerable)
        if self.enemy_bleed > 0:
            damage = int(damage * 1.33)

        return damage
    
    # ========================
        # NOVO: INTENT SYSTEM
    # ========================
    def generate_intent(self):

        if self.enemy_name == "Dragon Lord":
            self.intent = dragon_lord_intent(self)

        elif self.enemy_name == "Hydra":
            self.intent = hydra_intent(self)

        elif self.enemy_name == "Behemoth":
            self.intent = behemoth_intent(self)

        else:
            self.intent = {"type": "attack", "value": self.enemy_attack}


    # ========================
    # INIT DO COMBATE
    # ========================
    def __init__(self, data, player):

        self.player = player
        self.data = data
        
        # Buscar dados do monstro
        monster = get_monster(data)


        self.enemy_name = monster["name"]
        self.enemy_hp = monster["hp"]
        self.enemy_max_hp = monster["hp"]
        self.enemy_attack = monster["attack"]


        # Status effects do inimigo
        self.enemy_poison = 0
        self.enemy_burn = 0
        self.enemy_bleed = 0


        self.enemy_timer = 0  # controla quando inimigo ataca


        # novos intents
        self.intent = None
        self.generate_intent()

        # Buffs temporários do player
        self.temp_evade_bonus = 0
        self.temp_damage_bonus = 0
        self.temp_str = 0
        self.temp_str_turns = 0

        # Estado do combate
        self.player_turn = True
        self.combat_over = False

        # UI
        self.damage_texts = []
        self.hit_flash = 0
        self.shake = 0

        # Cooldowns
        self.skill_cooldowns = {}
        self.defense_cooldown = 0


        # ========================
        # ICONS DOS STATUS
        # ========================
        self.poison_icon = pygame.image.load("assets/icons/poison.png").convert_alpha()
        self.poison_icon = pygame.transform.scale(self.poison_icon, (24,24))

        self.burn_icon = pygame.image.load("assets/icons/burn.png").convert_alpha()
        self.burn_icon = pygame.transform.scale(self.burn_icon, (24,24))

        self.bleed_icon = pygame.image.load("assets/icons/bleed.png").convert_alpha()
        self.bleed_icon = pygame.transform.scale(self.bleed_icon, (24,24))


        # ========================
        # SPRITE DO INIMIGO
        # ========================
        name = self.enemy_name.lower().replace(" ", "_")
        path = f"assets/sprites/{name}.png"

        try:
            self.enemy_sprite = pygame.image.load(path).convert_alpha()
            self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (180,180))
        except:
            # fallback caso não exista sprite
            self.enemy_sprite = pygame.Surface((180,180))
            self.enemy_sprite.fill((200,50,50))


        # ========================
        # LAYOUT DOS BOTÕES
        # ========================
        self.button_w = 150
        self.button_h = 50
        self.gap_x = 20
        self.gap_y = 15

        cols = 3

        total_width = cols * self.button_w + (cols - 1) * self.gap_x
        self.start_x = COMBAT_CENTER_X - total_width // 2
        self.start_y = BUTTON_Y

        # Botão Attack
        self.attack_button = Button(self.start_x, self.start_y, self.button_w, self.button_h, "Attack")

        # Botão Defense
        self.defense_button = Button(
            self.start_x + (self.button_w + self.gap_x),
            self.start_y,
            self.button_w,
            self.button_h,
            "Defense"
        )

        # ========================
        # SKILL BUTTONS
        # ========================
        self.skill_buttons = []

        for i in range(MAX_SKILLS):

            x = self.start_x + i * (self.button_w + self.gap_x)
            y = self.start_y + self.button_h + self.gap_y

            if i < len(self.player.skills):

                skill_id = self.player.skills[i]

                btn = Button(
                    x,
                    y,
                    self.button_w,
                    self.button_h,
                    skill_id.replace("_", " ").title()
                )

                self.skill_cooldowns[skill_id] = 0

            else:
                btn = Button(x, y, self.button_w, self.button_h, "Locked")

            self.skill_buttons.append(btn)

        # Botão de vitória
        self.return_button = Button(0, BUTTON_Y, 300, 60, "Rewards")
        self.return_button.rect.centerx = COMBAT_CENTER_X


    # ========================
    # USAR SKILLS
    # ========================
    def use_skill(self, skill_id):

        # Cada skill aplica efeito e define cooldown
        if skill_id == "fireball":
            fireball(self)
            self.skill_cooldowns[skill_id] = 2

        elif skill_id == "power_strike":
            power_strike(self)
            self.skill_cooldowns[skill_id] = 3

        elif skill_id == "flaming_arrow":
            flaming_arrow(self)
            self.skill_cooldowns[skill_id] = 3

        elif skill_id == "evade":
            evade(self)
            self.skill_cooldowns[skill_id] = 2
        
        elif skill_id == "whirlwind":
            whirlwind(self)
            self.skill_cooldowns[skill_id] = 3

        elif skill_id == "berserk":
            berserk(self)
            self.skill_cooldowns[skill_id] = 4

        elif skill_id == "ice_blast":
            ice_blast(self)
            self.skill_cooldowns[skill_id] = 2

        elif skill_id == "lightning":
            lightning(self)
            self.skill_cooldowns[skill_id] = 3

        elif skill_id == "poison_arrow":
            poison_arrow(self)
            self.skill_cooldowns[skill_id] = 2

        elif skill_id == "rapid_fire":
            rapid_fire(self)
            self.skill_cooldowns[skill_id] = 3


    # (duplicado mas mantive como está)
    def deal_damage(self, damage):

        if self.enemy_bleed > 0:
            damage = int(damage * 1.33)

        return damage


    # ========================
    # INPUT (CLICKS)
    # ========================
    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            # Só podes agir no teu turno
            if not self.combat_over and self.player_turn:

                # ========================
                # ATTACK
                # ========================
                if self.attack_button.clicked(event):

                    # cálculo base
                    base_damage = self.player.attack + self.player.str + self.temp_str

                    # bonus temporário
                    if self.temp_damage_bonus > 0:
                        base_damage = int(base_damage * (1 + self.temp_damage_bonus))
                        self.temp_damage_bonus = 0

                    # crit
                    is_crit = random.random() < self.player.crit_chance
                    damage = base_damage * (self.player.crit_multiplier if is_crit else 1)

                    # aplicar efeitos (bleed etc)
                    damage = self.deal_damage(damage)

                    self.enemy_hp -= damage

                    # texto de dano
                    text = f"CRIT {damage}" if is_crit else str(damage)
                    color = (255,220,50) if is_crit else (255,50,50)

                    self.damage_texts.append(
                        DamageText(COMBAT_CENTER_X,110,text,color)
                    )

                    # efeitos visuais
                    self.hit_flash = 6
                    self.shake = 6

                    if self.enemy_hp < 0:
                        self.enemy_hp = 0

                    self.player_turn = False

                # ========================
                # SKILLS
                # ========================
                for i, button in enumerate(self.skill_buttons):

                    if i < len(self.player.skills):

                        skill_id = self.player.skills[i]

                        if button.clicked(event) and self.skill_cooldowns[skill_id] == 0:
                            self.use_skill(skill_id)

                # ========================
                # DEFENSE
                # ========================
                if self.defense_button.clicked(event) and self.defense_cooldown == 0:

                    if self.player.vocation == "warrior":
                        shield_block(self)

                    elif self.player.vocation == "mage":
                        mana_shield(self)

                    elif self.player.vocation == "hunter":
                        self.temp_evade_bonus = 0.1
                        self.temp_damage_bonus = 0.5

                        self.damage_texts.append(
                            DamageText(COMBAT_CENTER_X, 330, "Focus", (200,200,100))
                        )

                        self.player_turn = False

                    self.defense_cooldown = 1

            # Botão de vitória
            elif self.combat_over and self.return_button.clicked(event):
                return ("VICTORY", self.data)

        if self.player.hp <= 0:
            return "GAME_OVER"


    # ========================
    # UPDATE DO COMBATE
    # ========================
    def update(self):

        # Turno do inimigo
        if not self.player_turn and not self.combat_over and self.enemy_hp > 0:
            self.enemy_timer += 1

            if self.enemy_timer > 30: 

                # ========================
                # POISON
                # ========================
                if self.enemy_poison > 0:
                    poison_damage = self.enemy_poison
                    self.enemy_hp -= poison_damage
                    self.enemy_poison -= 1

                    self.damage_texts.append(
                        DamageText(COMBAT_CENTER_X, 80, f"Poison {poison_damage}", (100,255,100))
                    )
                    
                if self.enemy_hp <= 0:
                    self.combat_over = True
                    return

                # cooldowns
                for skill in self.skill_cooldowns:
                    if self.skill_cooldowns[skill] > 0:
                        self.skill_cooldowns[skill] -= 1

                if self.defense_cooldown > 0:
                    self.defense_cooldown -= 1
                
                # ========================
                # EVADE
                # ========================
                evade_chance = 0

                if self.player.passive["name"] == "Hunter Instinct":
                    evade_chance += 0.2

                evade_chance += self.temp_evade_bonus

                if random.random() < evade_chance:
                    self.damage_texts.append(
                        DamageText(COMBAT_CENTER_X, 330, "Evade!", (200,200,200))
                    )
                    self.temp_evade_bonus = 0
                    self.player_turn = True
                    self.enemy_timer = 0

                    self.generate_intent() # <------ AQUIs
                    
                    return


                intent = self.intent

                if intent["type"] == "attack":
                    attack = intent["value"]
                else:
                    attack = self.enemy_attack  # fallback para não crashar

                # Burn reduz ataque
                if self.enemy_burn > 0:
                    attack = int(attack * 0.67)

                # ========================
                # DAMAGE PLAYER
                # ========================
                block = self.player.block
                blocked = min(block, attack)
                damage = attack - blocked

                self.player.take_damage(damage)

                # textos
                if damage > 0:
                    self.damage_texts.append(
                        DamageText(COMBAT_CENTER_X,330,str(damage),(255,50,50))
                    )

                if blocked > 0:
                    self.damage_texts.append(
                        DamageText(COMBAT_CENTER_X,300,str(blocked),(150,150,150))
                    )

                self.player.block = 0

                # ========================
                # DOTS (burn / bleed)
                # ========================
                if self.enemy_burn > 0:
                    burn_damage = self.enemy_burn
                    self.enemy_hp -= burn_damage
                    self.enemy_burn -= 1

                if self.enemy_bleed > 0:
                    bleed_damage = self.enemy_bleed
                    self.enemy_hp -= bleed_damage
                    self.enemy_bleed -= 1

                # ========================
                # BUFF DECAY
                # ========================
                if self.temp_str_turns > 0:
                    self.temp_str_turns -= 1

                    if self.temp_str_turns == 0:
                        self.temp_str = 0

                self.player_turn = True
                self.enemy_timer = 0
                self.generate_intent()

                # mana regen passivo
                if self.player.passive["name"] == "Arcane Power":
                    self.player.restore_mana(2)

        if self.enemy_hp <= 0:
            self.combat_over = True

        # limpar textos mortos
        self.damage_texts = [t for t in self.damage_texts if t.alive()]

        # efeitos visuais
        if self.hit_flash > 0:
            self.hit_flash -= 1

        if self.shake > 0:
            self.shake -= 1


    # ========================
    # DRAW (RENDER)
    # ========================
    def draw(self, screen, font):

        # shake effect
        offset_x = random.randint(-5,5) if self.shake > 0 else 0
        offset_y = random.randint(-5,5) if self.shake > 0 else 0

        passive_x = self.start_x + 2 * (self.button_w + self.gap_x)
        passive_y = self.start_y

        # inimigo
        enemy_rect = self.enemy_sprite.get_rect(center=(COMBAT_CENTER_X + offset_x, ENEMY_Y + offset_y))
        screen.blit(self.enemy_sprite, enemy_rect)

        # HP inimigo
        hp_y = enemy_rect.top - 20
        draw_hp_bar(screen, COMBAT_CENTER_X-150, hp_y, 300, 25, self.enemy_hp, self.enemy_max_hp, font)


        # nome enemy
        name_text = font.render(self.enemy_name, True, (255,255,255))
        name_x = COMBAT_CENTER_X + 150 - name_text.get_width()
        name_y = hp_y + 30
        screen.blit(name_text, (name_x, name_y))

        # ========================
        # STATUS ICONS
        # ========================
        status_x = COMBAT_CENTER_X - 150
        status_y = hp_y + 30
        x = status_x
        gap = 60

        if self.enemy_poison > 0:
            screen.blit(self.poison_icon, (x, status_y))
            x += gap

        if getattr(self, "enemy_burn", 0) > 0:
            screen.blit(self.burn_icon, (x, status_y))
            x += gap

        if getattr(self, "enemy_bleed", 0) > 0:
            screen.blit(self.bleed_icon, (x, status_y))
            x += gap

        # intenção inimigo
        display_attack = self.enemy_attack
        if self.enemy_burn > 0:
            display_attack = int(self.enemy_attack * 0.67)

        screen.blit(font.render(f"Intent: Attack {display_attack}",True,(255,200,200)),(COMBAT_CENTER_X-120,230))

        # HP player
        draw_hp_bar(screen, COMBAT_CENTER_X-150, PLAYER_HP_Y, 300, 25, self.player.hp, self.player.max_hp, font)

        # ========================
        # BOTÕES
        # ========================
        if not self.combat_over:

            self.attack_button.draw(screen,font)
            self.defense_button.draw(screen,font)

            for i, button in enumerate(self.skill_buttons):

                button.draw(screen,font)

                if i < len(self.player.skills):

                    skill_id = self.player.skills[i]
                    cd = self.skill_cooldowns.get(skill_id, 0)

                    if cd > 0:
                        cd_text = font.render(f"CD {cd}", True, (255,100,100))
                        screen.blit(cd_text, (button.rect.x, button.rect.y - 18))

        else:
            screen.blit(font.render("Victory!",True,(255,255,0)),(COMBAT_CENTER_X-50,300))
            self.return_button.draw(screen,font)

        # turno
        if not self.combat_over:
            turn = "Your Turn" if self.player_turn else "Enemy Turn"
            color = (0,255,0) if self.player_turn else (255,0,0)

            screen.blit(font.render(turn,True,color),(COMBAT_CENTER_X-80,TURN_TEXT_Y))

        # textos de dano
        for text in self.damage_texts:
            text.draw(screen,font)