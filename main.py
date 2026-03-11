import pygame
import sys

from states.map_state import MapState
from states.combat_state import CombatState
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

player_hp = 50

map_state = MapState()
state = map_state

running = True

player = Player()
floor = 1

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        new_state = state.handle_event(event)

        if isinstance(new_state, tuple):
            state_name, tier = new_state
            if state_name == "COMBAT":
                state = CombatState(tier, player)

        elif new_state == "MAP":
            state = map_state

        elif new_state == "REST":
            heal = int(player.max_hp * 0.3)
            player.hp = min(player.hp + heal, player.max_hp)
            state = map_state    


    state.update()

    screen.fill((44,44,44))

    # draw map/combat
    state.draw(screen, font)

    # side panel
    pygame.draw.rect(screen, (80,80,80), side_panel)

    screen.blit(font.render("PLAYER", True, (255,255,255)), (720,40))
    screen.blit(font.render(f"HP: {player.hp}/{player.max_hp}", True, (255,255,255)), (720,80))
    screen.blit(font.render(f"Mana: {player.mana}", True, (255,255,255)), (720,120))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()