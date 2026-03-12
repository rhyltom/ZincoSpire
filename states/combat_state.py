import pygame
import random

from entities.monsters import get_monster_by_difficulty
from ui.damage_text import DamageText
from ui.button import Button

from skills.skills import (
    fireball,
    power_strike,
    power_shot,
    shield_block,
    mana_shield,
    evade
)

# ========================
# LAYOUT CONSTANTS
# ========================

SCREEN_WIDTH = 1000
PANEL_WIDTH = 280

COMBAT_WIDTH = SCREEN_WIDTH - PANEL_WIDTH
COMBAT_CENTER_X = COMBAT_WIDTH // 2

ENEMY_Y = 120
ENEMY_HP_Y = 160

PLAYER_HP_Y = 350
PLAYER_LABEL_Y = 320

TURN_TEXT_Y = 410
BUTTON_Y = 450


def draw_hp_bar(screen, x, y, width, height, current_hp, max_hp):

    ratio = current_hp / max_hp

    pygame.draw.rect(screen, (120,0,0), (x, y, width, height))
    pygame.draw.rect(screen, (0,200,0), (x, y, width * ratio, height))
    pygame.draw.rect(screen, (255,255,255), (x, y, width, height), 2)


class CombatState:

    def __init__(self, tier, player):

        monster = get_monster_by_difficulty(tier)

        self.player = player
        self.tier = tier

        # ========================
        # ENEMY STATS
        # ========================

        self.enemy_name = monster["name"]
        self.enemy_hp = monster["hp"]
        self.enemy_max_hp = monster["hp"]
        self.enemy_attack = monster["attack"]

        # ========================
        # COMBAT STATE
        # ========================

        self.enemy_timer = 0
        self.player_turn = True
        self.combat_over = False

        self.damage_texts = []

        self.hit_flash = 0
        self.shake = 0

        # cooldowns
        self.skill_cooldown = 0
        self.defense_cooldown = 0

        # ========================
        # LOAD ENEMY SPRITE
        # ========================

        name = self.enemy_name.lower().replace(" ", "_")
        path = f"assets/sprites/{name}.png"

        try:
            self.enemy_sprite = pygame.image.load(path).convert_alpha()
            self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (180,180))
        except:
            self.enemy_sprite = None


        # ========================
        # CLASS SKILL NAMES
        # ========================

        if player.vocation == "warrior":
            skill_name = "Power Strike"
            defense_name = "Shield Block"

        elif player.vocation == "hunter":
            skill_name = "Power Shot"
            defense_name = "Evade"

        elif player.vocation == "mage":
            skill_name = "Fireball"
            defense_name = "Mana Shield"


        # ========================
        # BUTTON LAYOUT
        # ========================

        button_width = 180
        gap = 20

        start_x = COMBAT_CENTER_X - (button_width*3 + gap*2)//2

        self.attack_button = Button(start_x, BUTTON_Y, button_width, 50, "Attack")
        self.skill_button = Button(start_x + button_width + gap, BUTTON_Y, button_width, 50, skill_name)
        self.defense_button = Button(start_x + (button_width + gap)*2, BUTTON_Y, button_width, 50, defense_name)

        self.return_button = Button(0, BUTTON_Y, 300, 60, "Rewards")
        self.return_button.rect.centerx = COMBAT_CENTER_X


    # ========================
    # HANDLE INPUT
    # ========================

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if not self.combat_over and self.player_turn:

                if self.attack_button.clicked(event):

                    base_damage = self.player.attack + self.player.str
                    is_crit = random.random() < self.player.crit_chance

                    damage = base_damage

                    if is_crit:
                        damage *= self.player.crit_multiplier

                    self.enemy_hp -= damage

                    text = f"CRIT {damage}" if is_crit else str(damage)
                    color = (255,220,50) if is_crit else (255,50,50)

                    self.damage_texts.append(
                        DamageText(COMBAT_CENTER_X,110,text,color)
                    )

                    self.hit_flash = 6
                    self.shake = 6

                    if self.enemy_hp < 0:
                        self.enemy_hp = 0

                    self.player_turn = False


                elif self.skill_button.clicked(event) and self.skill_cooldown == 0:

                    if self.player.vocation == "mage":
                        fireball(self)
                        self.skill_cooldown = 2

                    elif self.player.vocation == "hunter":
                        power_shot(self)
                        self.skill_cooldown = 3

                    elif self.player.vocation == "warrior":
                        power_strike(self)
                        self.skill_cooldown = 4


                elif self.defense_button.clicked(event) and self.defense_cooldown == 0:

                    if self.player.vocation == "warrior":
                        shield_block(self)
                        self.defense_cooldown = 1

                    elif self.player.vocation == "mage":
                        mana_shield(self)
                        self.defense_cooldown = 1

                    elif self.player.vocation == "hunter":
                        evade(self)
                        self.defense_cooldown = 1


            elif self.combat_over and self.return_button.clicked(event):

                return ("VICTORY", self.tier)


        if self.player.hp <= 0:
            return "GAME_OVER"


    # ========================
    # UPDATE COMBAT
    # ========================

    def update(self):

        if not self.player_turn and not self.combat_over and self.enemy_hp > 0:

            self.enemy_timer += 1

            if self.enemy_timer > 30:

                # reduce cooldowns each turn
                if self.skill_cooldown > 0:
                    self.skill_cooldown -= 1

                if self.defense_cooldown > 0:
                    self.defense_cooldown -= 1


                if self.player.evade:

                    if random.random() < 0.5:

                        self.damage_texts.append(
                            DamageText(COMBAT_CENTER_X,330,"Miss",(200,200,200))
                        )

                        self.player.evade = False
                        self.player_turn = True
                        self.enemy_timer = 0
                        return

                    self.player.evade = False


                attack = self.enemy_attack
                block = self.player.block

                blocked_damage = min(block, attack)
                real_damage = attack - blocked_damage

                self.player.take_damage(real_damage)

                if real_damage > 0:
                    self.damage_texts.append(
                        DamageText(COMBAT_CENTER_X,330,str(real_damage),(255,50,50))
                    )

                if blocked_damage > 0:
                    self.damage_texts.append(
                        DamageText(COMBAT_CENTER_X,300,str(blocked_damage),(150,150,150))
                    )

                self.player.block = 0

                self.player_turn = True
                self.enemy_timer = 0


        if self.enemy_hp <= 0:
            self.combat_over = True


        for text in self.damage_texts:
            text.update()

        self.damage_texts = [
            t for t in self.damage_texts if t.alive()
        ]


        if self.hit_flash > 0:
            self.hit_flash -= 1

        if self.shake > 0:
            self.shake -= 1


    # ========================
    # DRAW COMBAT
    # ========================

    def draw(self, screen, font):

        offset_x = 0
        offset_y = 0

        if self.shake > 0:
            offset_x = random.randint(-5,5)
            offset_y = random.randint(-5,5)


        if self.enemy_sprite:

            rect = self.enemy_sprite.get_rect(center=(COMBAT_CENTER_X + offset_x, ENEMY_Y + offset_y))
            screen.blit(self.enemy_sprite, rect)

            if self.hit_flash > 0:
                flash = pygame.Surface(self.enemy_sprite.get_size())
                flash.fill((255,50,50))
                flash.set_alpha(120)
                screen.blit(flash, rect)


        draw_hp_bar(screen, COMBAT_CENTER_X-150, ENEMY_HP_Y, 300, 25, self.enemy_hp, self.enemy_max_hp)
        draw_hp_bar(screen, COMBAT_CENTER_X-150, PLAYER_HP_Y, 300, 25, self.player.hp, self.player.max_hp)


        player_text = font.render("Player",True,(255,255,255))
        screen.blit(player_text,(COMBAT_CENTER_X-100,PLAYER_LABEL_Y))


        intent_text = font.render(
            f"Intent: Attack {self.enemy_attack}",
            True,
            (255,200,200)
        )
        screen.blit(intent_text,(COMBAT_CENTER_X-120,210))


        if not self.combat_over:

            self.attack_button.draw(screen,font)
            self.skill_button.draw(screen,font)
            self.defense_button.draw(screen,font)

        else:

            victory = font.render("Victory!",True,(255,255,0))
            screen.blit(victory,(COMBAT_CENTER_X-50,300))

            self.return_button.draw(screen,font)


        if not self.combat_over:

            if self.player_turn:
                turn_text = font.render("Your Turn",True,(0,255,0))
            else:
                turn_text = font.render("Enemy Turn",True,(255,0,0))

            screen.blit(turn_text,(COMBAT_CENTER_X-80,TURN_TEXT_Y))


        # cooldown indicators
        if self.skill_cooldown > 0:

            cd_text = font.render(f"CD {self.skill_cooldown}", True, (255,100,100))
            screen.blit(cd_text, (self.skill_button.rect.x, self.skill_button.rect.y - 20))


        if self.defense_cooldown > 0:

            cd_text = font.render(f"CD {self.defense_cooldown}", True, (255,100,100))
            screen.blit(cd_text, (self.defense_button.rect.x, self.defense_button.rect.y - 20))


        for text in self.damage_texts:
            text.draw(screen,font)