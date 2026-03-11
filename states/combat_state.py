import pygame
from entities.monsters import get_monster_by_difficulty
from ui.damage_text import DamageText
from ui.button import Button


def draw_hp_bar(screen, x, y, width, height, current_hp, max_hp):

    ratio = current_hp / max_hp

    pygame.draw.rect(screen, (120,0,0), (x, y, width, height))
    pygame.draw.rect(screen, (0,200,0), (x, y, width * ratio, height))

    pygame.draw.rect(screen, (255,255,255), (x, y, width, height), 2)


class CombatState:

    def __init__(self, tier, player): 

        monster = get_monster_by_difficulty(tier)

        self.enemy_name = monster["name"]
        self.enemy_hp = monster["hp"]
        self.enemy_max_hp = monster["hp"]
        self.enemy_timer = 0
        self.enemy_attack = monster["attack"]

        self.combat_over = False

        name = self.enemy_name.lower().replace(" ", "_")
        path = f"assets/sprites/{name}.png"

        self.big_font = pygame.font.SysFont(None, 60)
        try:
            self.enemy_sprite = pygame.image.load(path).convert_alpha()
            self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (180,180))
            
        except:
            self.enemy_sprite = None

        self.hit_flash = 0
        self.shake = 0    

        
        self.damage_texts = []
        self.player = player
        self.attack_button = Button(220, 450, 200, 50, "Attack")
        self.defend_button = Button(430, 450, 200, 50, "Defend")
        self.return_button = Button(0, 450, 300, 60, "Return to Map")
        self.return_button.rect.centerx = 400
        self.player_turn = True

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.player_turn and self.attack_button.clicked(event):
                # Player attack
                damage = self.player.attack
                self.enemy_hp -= damage
                self.hit_flash = 6
                self.shake = 6
                self.damage_texts.append(
                    DamageText(380, 150, str(damage), (255,50,50))
                )

                if self.enemy_hp < 0:
                    self.enemy_hp = 0

                self.player_turn = False



            if self.player_turn and self.defend_button.clicked(event):
                self.player.block = 5
                self.player_turn = False    

        if self.combat_over and self.return_button.clicked(event):
            return "MAP"



        # Enemy turn
        if not self.player_turn and self.enemy_hp > 0:

            self.enemy_timer += 1

            if self.enemy_timer > 30:  # meio segundo aprox

                self.player.take_damage(self.enemy_attack)

                self.player_turn = True
                self.enemy_timer = 0

        # End combat
        if self.enemy_hp <= 0:
            self.combat_over = True

        if self.player.hp <= 0:
            return "GAME_OVER"






    def update(self):

    # enemy turn
        if not self.player_turn and self.enemy_hp > 0:
            self.enemy_timer += 1

            if self.enemy_timer > 30:
                color = (255,50,50)

                attack = self.enemy_attack
                block = self.player.block
                blocked_damage = min(block, attack)
                real_damage = attack - blocked_damage

                # aplicar dano real
                self.player.take_damage(real_damage)

                # mostrar dano recebido
                if real_damage > 0:
                    self.damage_texts.append(
                        DamageText(380, 330, str(real_damage), (255,50,50))
                )
                # mostrar dano bloqueado
                if blocked_damage > 0:
                    self.damage_texts.append(
                        DamageText(380, 300, str(blocked_damage), (150,150,150))
                )
                # reset block
                self.player.block = 0

                 

                self.player_turn = True
                self.enemy_timer = 0

        # update floating damage numbers
        for text in self.damage_texts:
            text.update()
        # REMOVE DEAD TEXTS    
        self.damage_texts = [
            t for t in self.damage_texts if t.alive()
        ]   

        if self.hit_flash > 0:
            self.hit_flash -= 1
        if self.shake > 0:
            self.shake -= 1




    def draw(self, screen, font):


        if self.enemy_sprite:
            offset_x = 0
            offset_y = 0

            if self.shake > 0:
                import random
                offset_x = random.randint(-5,5)
                offset_y = random.randint(-5,5)

            rect = self.enemy_sprite.get_rect(center=(400 + offset_x,120 + offset_y))
            screen.blit(self.enemy_sprite, rect)


        if self.hit_flash > 0:
            flash = pygame.Surface(self.enemy_sprite.get_size())
            flash.fill((255,50,50))
            flash.set_alpha(120)
            screen.blit(flash, rect)



        # Enemy HP bar
        draw_hp_bar(screen, 250, 160, 300, 25, self.enemy_hp, self.enemy_max_hp)

        # Player HP bar
        draw_hp_bar(screen, 250, 350, 300, 25, self.player.hp, self.player.max_hp)

        player_text = font.render("Player", True, (255,255,255))
        screen.blit(player_text, (300,320))

        # Enemy intent
        intent_text = font.render(
            f"Intent: Attack {self.enemy_attack}", True, (255,200,200)
        )
        screen.blit(intent_text, (300,210))



        if not self.combat_over:
            # Fight Buttons
            self.attack_button.draw(screen, font)
            self.defend_button.draw(screen, font)
        else:
            victory = font.render("Victory!", True, (255,255,0))
            screen.blit(victory, (400,300))

            self.return_button.draw(screen, font)

        # Turn text
        if not self.combat_over:
            if self.player_turn:
                turn_text = font.render("Your Turn", True, (0,255,0))
            else:
                turn_text = font.render("Enemy Turn", True, (255,0,0))
            screen.blit(turn_text, (320,410))