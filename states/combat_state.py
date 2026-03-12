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

        # visual effects
        self.hit_flash = 0
        self.shake = 0

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
        # UI BUTTONS
        # ========================

        self.attack_button = Button(180, 450, 180, 50, "Attack")
        self.skill_button = Button(380, 450, 180, 50, "Skill")
        self.defense_button = Button(580, 450, 180, 50, "Defense")

        self.return_button = Button(0, 450, 300, 60, "Rewards")
        self.return_button.rect.centerx = 400


    # ========================
    # HANDLE INPUT
    # ========================

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if not self.combat_over and self.player_turn:

                # ========================
                # BASIC ATTACK
                # ========================

                if self.attack_button.clicked(event):

                    base_damage = self.player.attack + self.player.str

                    is_crit = random.random() < self.player.crit_chance

                    damage = base_damage

                    if is_crit:
                        damage *= self.player.crit_multiplier

                    self.enemy_hp -= damage

                    if is_crit:
                        text = f"CRIT {damage}"
                        color = (255,220,50)
                    else:
                        text = str(damage)
                        color = (255,50,50)

                    self.damage_texts.append(
                        DamageText(400,110,text,color)
                    )

                    self.hit_flash = 6
                    self.shake = 6

                    if self.enemy_hp < 0:
                        self.enemy_hp = 0

                    self.player_turn = False


                # ========================
                # SKILLS
                # ========================

                elif self.skill_button.clicked(event):

                    if self.player.vocation == "mage":
                        fireball(self)

                    elif self.player.vocation == "hunter":
                        power_shot(self)

                    elif self.player.vocation == "warrior":
                        power_strike(self)


                # ========================
                # DEFENSE PER CLASS
                # ========================

                elif self.defense_button.clicked(event):

                    if self.player.vocation == "warrior":
                        shield_block(self)

                    elif self.player.vocation == "mage":
                        mana_shield(self)

                    elif self.player.vocation == "hunter":
                        evade(self)


            elif self.combat_over and self.return_button.clicked(event):

                return ("VICTORY", self.tier)


        if self.player.hp <= 0:
            return "GAME_OVER"


    # ========================
    # UPDATE COMBAT
    # ========================

    def update(self):

        # enemy turn
        if not self.player_turn and not self.combat_over and self.enemy_hp > 0:

            self.enemy_timer += 1

            if self.enemy_timer > 30:

                # ========================
                # HUNTER EVADE CHECK
                # ========================

                if self.player.evade:

                    if random.random() < 0.5:

                        self.damage_texts.append(
                            DamageText(400,330,"Miss",(200,200,200))
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
                        DamageText(400,330,str(real_damage),(255,50,50))
                    )

                if blocked_damage > 0:
                    self.damage_texts.append(
                        DamageText(400,300,str(blocked_damage),(150,150,150))
                    )

                self.player.block = 0

                self.player_turn = True
                self.enemy_timer = 0


        # end combat
        if self.enemy_hp <= 0:
            self.combat_over = True


        # update floating numbers
        for text in self.damage_texts:
            text.update()

        self.damage_texts = [
            t for t in self.damage_texts if t.alive()
        ]


        # visual effects
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


        # enemy sprite
        if self.enemy_sprite:

            rect = self.enemy_sprite.get_rect(center=(400 + offset_x,120 + offset_y))
            screen.blit(self.enemy_sprite, rect)

            if self.hit_flash > 0:
                flash = pygame.Surface(self.enemy_sprite.get_size())
                flash.fill((255,50,50))
                flash.set_alpha(120)
                screen.blit(flash, rect)


        # HP bars
        draw_hp_bar(screen,250,160,300,25,self.enemy_hp,self.enemy_max_hp)
        draw_hp_bar(screen,250,350,300,25,self.player.hp,self.player.max_hp)


        # labels
        player_text = font.render("Player",True,(255,255,255))
        screen.blit(player_text,(300,320))

        intent_text = font.render(
            f"Intent: Attack {self.enemy_attack}",
            True,
            (255,200,200)
        )
        screen.blit(intent_text,(300,210))


        # buttons
        if not self.combat_over:

            self.attack_button.draw(screen,font)
            self.skill_button.draw(screen,font)
            self.defense_button.draw(screen,font)

        else:

            victory = font.render("Victory!",True,(255,255,0))
            screen.blit(victory,(370,300))

            self.return_button.draw(screen,font)


        # turn text
        if not self.combat_over:

            if self.player_turn:
                turn_text = font.render("Your Turn",True,(0,255,0))
            else:
                turn_text = font.render("Enemy Turn",True,(255,0,0))

            screen.blit(turn_text,(320,410))


        # damage numbers
        for text in self.damage_texts:
            text.draw(screen,font)