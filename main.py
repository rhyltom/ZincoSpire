import pygame
import sys

from states.map_state import MapState
from states.combat_state import CombatState
from states.game_over_state import GameOverState
from states.reward_state import RewardState
from states.vocation_state import VocationSelect
from states.shop_state import ShopState
from states.skill_select_state import SkillSelectState

from entities.player import Player


pygame.init()

WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zinco Spire")

from entities.map_node import load_icons
load_icons()

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 28)

side_panel = pygame.Rect(700, 20, 280, 560)


# ========================
# icons = 24x24
atk_icon = pygame.image.load("assets/icons/atk.png").convert_alpha()
str_icon = pygame.image.load("assets/icons/str.png").convert_alpha()
mgc_icon = pygame.image.load("assets/icons/mgc.png").convert_alpha()
hp_icon = pygame.image.load("assets/icons/hp.png").convert_alpha()
mana_icon = pygame.image.load("assets/icons/mana.png").convert_alpha()
gold_icon = pygame.image.load("assets/icons/gold.png").convert_alpha()


atk_icon = pygame.transform.scale(atk_icon, (24,24))
str_icon = pygame.transform.scale(str_icon, (24,24))
mgc_icon = pygame.transform.scale(mgc_icon, (24,24))
hp_icon = pygame.transform.scale(hp_icon, (24,24))
mana_icon = pygame.transform.scale(mana_icon, (24,24))
gold_icon = pygame.transform.scale(gold_icon, (24,24))



# ========================
# INITIAL STATES
player = None

current_act = 1
MAX_ACT = 3

map_state = MapState(current_act)
next_map = None
state = VocationSelect()

running = True


# ========================
# MAIN LOOP
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        new_state = state.handle_event(event)


        # ========================
        # STATES THAT RETURN TUPLES
        if isinstance(new_state, tuple):

            state_name = new_state[0]


            # ========================
            # START GAME (CHOOSE CLASS)
            if state_name == "START_GAME":

                vocation = new_state[1]

                player = Player(vocation)
                current_act = 1

                map_state = MapState(current_act)
                state = map_state

                


            # ========================
            # COMBAT
            elif state_name == "COMBAT":

                data = new_state[1]

                state = CombatState(data, player)


            # ========================
            # VICTORY → REWARD
            elif state_name == "VICTORY":

                data = new_state[1]

                    # se for boss → próximo act
                if data.get("type") == "boss":
                    player.gold += 50
                    player.hp = player.max_hp

                    # boss final → acaba logo
                    if current_act >= MAX_ACT:
                        print("YOU WIN THE GAME!")
                        state = GameOverState(player)

                    else:
                        # guarda próximo act
                        current_act += 1
                        next_map = MapState(current_act)
                        state = SkillSelectState(player)

                else:
                        state = RewardState(player, data)


        # ========================
        # SIMPLE STATES
        elif new_state == "MAP":
            if next_map:
                map_state = next_map
                next_map = None
            state = map_state


        # ========================
        # REST (CAMPFIRE)
        elif new_state == "REST":

            heal = int(player.max_hp * 0.3)

            player.hp = min(player.hp + heal, player.max_hp)

            state = map_state


        # ========================
        # SHOP
        elif new_state == "SHOP":

            state = ShopState(player)


        # ========================
        # RESTART GAME
        elif new_state == "RESTART":

            player = None
            current_act = 1

            map_state = MapState(current_act)
            state = VocationSelect()


    # ========================
    # GAME OVER CHECK
    # ========================

    if player and player.hp <= 0 and not isinstance(state, GameOverState):

        state = GameOverState(player)


    state.update()


    # ========================
    # DRAW
    screen.fill((44,44,44))


    # SIDE PANEL
    pygame.draw.rect(screen, (80,80,80), side_panel)


    # CURRENT STATE
    state.draw(screen, font)


    # ========================
    # PLAYER UI
    if player:

        
        screen.blit(font.render("PLAYER", True, (255,255,255)), (720,40))

        screen.blit(hp_icon, (720,80))
        screen.blit(font.render(f"{player.hp}/{player.max_hp}", True, (255,255,255)), (750,80))

        screen.blit(mana_icon, (720,120))
        screen.blit(font.render(str(player.mana), True, (255,255,255)), (750,120))

        screen.blit(gold_icon, (720,160))
        screen.blit(font.render(str(player.gold), True, (255,215,0)), (750,160))

        screen.blit(atk_icon, (720,200))
        screen.blit(font.render(str(player.attack), True, (255,255,255)), (750,200))
        
        screen.blit(str_icon, (720,240))
        screen.blit(font.render(str(player.str), True, (255,255,255)), (750,240))

        screen.blit(mgc_icon, (720,280))
        screen.blit(font.render(str(player.mgc), True, (255,255,255)), (750,280))


        # ========================
        # ITEMS
        y = 340

        for item in player.items:

            try:

                icon = pygame.image.load(f"items/{item['icon']}").convert_alpha()

                icon = pygame.transform.scale(icon, (32,32))

                screen.blit(icon, (720, y))

            except:

                pygame.draw.rect(screen, (200,200,200), (720, y, 32, 32))


            name = font.render(item["name"], True, (255,255,255))
            screen.blit(name, (760, y))

            desc = font.render(item["desc"], True, (180,180,180))
            screen.blit(desc, (760, y+18))

            y += 45


    pygame.display.flip()

    clock.tick(60)


pygame.quit()
sys.exit()