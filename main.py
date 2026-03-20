import pygame
import sys

from states.map_state import MapState
from states.combat_state import CombatState
from states.game_over_state import GameOverState
from states.reward_state import RewardState
from states.vocation_state import VocationSelect
from states.shop_state import ShopState

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

current_act = 1
MAX_ACT = 3

# ========================
# INITIAL STATES
# ========================

player = None
map_state = MapState(current_act)

state = VocationSelect()

running = True


# ========================
# MAIN LOOP
# ========================

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        new_state = state.handle_event(event)


        # ========================
        # STATES THAT RETURN TUPLES
        # ========================

        if isinstance(new_state, tuple):

            state_name = new_state[0]


            # ========================
            # START GAME (CHOOSE CLASS)
            # ========================

            if state_name == "START_GAME":

                vocation = new_state[1]

                player = Player(vocation)

                map_state = MapState(current_act)

                state = map_state


            # ========================
            # COMBAT
            # ========================

            elif state_name == "COMBAT":

                data = new_state[1]

                state = CombatState(data, player)


            # ========================
            # VICTORY → REWARD
            # ========================

            elif state_name == "VICTORY":

                data = new_state[1]
                    # se for boss → próximo act
                if isinstance(data, dict) and data.get("type") == "boss":
                    current_act += 1
                    if current_act > MAX_ACT:
                        print("YOU WIN THE GAME!")
                        state = VocationSelect()  # ou victory screen
                    else:
                        map_state = MapState(current_act)
                        state = map_state


                else:
                        state = RewardState(player, data)


        # ========================
        # SIMPLE STATES
        # ========================

        elif new_state == "MAP":

            state = map_state


        # ========================
        # REST (CAMPFIRE)
        # ========================

        elif new_state == "REST":

            heal = int(player.max_hp * 0.3)

            player.hp = min(player.hp + heal, player.max_hp)

            state = map_state


        # ========================
        # SHOP
        # ========================

        elif new_state == "SHOP":

            state = ShopState(player)


        # ========================
        # RESTART GAME
        # ========================

        elif new_state == "RESTART":

            player = None

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
    # ========================

    screen.fill((44,44,44))


    # SIDE PANEL
    pygame.draw.rect(screen, (80,80,80), side_panel)


    # CURRENT STATE
    state.draw(screen, font)


    # ========================
    # PLAYER UI
    # ========================

    if player:

        screen.blit(font.render("PLAYER", True, (255,255,255)), (720,40))

        screen.blit(font.render(f"HP: {player.hp}/{player.max_hp}", True, (255,255,255)), (720,80))

        screen.blit(font.render(f"Mana: {player.mana}", True, (255,255,255)), (720,120))

        screen.blit(font.render(f"Gold: {player.gold}", True, (255,215,0)), (720,160))

        screen.blit(font.render(f"ATK: {player.attack}", True, (255,255,255)), (720,200))

        screen.blit(font.render(f"STR: {player.str}", True, (255,255,255)), (720,240))

        screen.blit(font.render(f"MGC: {player.mgc}", True, (255,255,255)), (720,280))


        # ========================
        # ITEMS
        # ========================

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