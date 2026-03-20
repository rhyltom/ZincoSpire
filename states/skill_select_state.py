import pygame
import random

from ui.button import Button

# ========================
# LAYOUT CONSTANTS
# ========================

SCREEN_WIDTH = 1000
PANEL_WIDTH = 280

COMBAT_WIDTH = SCREEN_WIDTH - PANEL_WIDTH
COMBAT_CENTER_X = COMBAT_WIDTH // 2


SKILL_POOL = {
    "warrior": [
        {"id": "power_strike", "name": "Power Strike"},
        {"id": "whirlwind", "name": "Whirlwind"},
        {"id": "berserk", "name": "Berserk"},
    ],
    "mage": [
        {"id": "fireball", "name": "Fireball"},
        {"id": "ice_blast", "name": "Ice Blast"},
        {"id": "lightning", "name": "Lightning"},
    ],
    "hunter": [
        {"id": "power_shot", "name": "Power Shot"},
        {"id": "poison_arrow", "name": "Poison Arrow"},
        {"id": "rapid_fire", "name": "Rapid Fire"},
    ]
}


class SkillSelectState:

    def __init__(self, player):

        self.player = player

        # remove skills já adquiridas
        pool = SKILL_POOL.get(player.vocation, [])

        available = [s for s in pool if s["id"] not in player.skills]

        self.options = random.sample(available, min(3, len(available)))

        self.buttons = []

        # ========================
        # LAYOUT DINÂMICO
        # ========================

        button_w = 160
        button_h = 60
        gap = 20

        total_width = len(self.options) * button_w + (len(self.options) - 1) * gap

        start_x = COMBAT_CENTER_X - total_width // 2
        y = 260

        for i, skill in enumerate(self.options):

            btn = Button(
                start_x + i * (button_w + gap),
                y,
                button_w,
                button_h,
                skill["name"]
            )

            self.buttons.append(btn)


    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            for i, btn in enumerate(self.buttons):

                if btn.clicked(event):

                    skill = self.options[i]

                    self.player.skills.append(skill["id"])

                    return "MAP"


    def update(self):
        pass


    def draw(self, screen, font):

        # ========================
        # TITLE (CENTRADO)
        # ========================

        title = font.render("Choose a Skill", True, (255,255,255))
        title_rect = title.get_rect(center=(COMBAT_CENTER_X, 180))
        screen.blit(title, title_rect)

        # ========================
        # BUTTONS
        # ========================

        for btn in self.buttons:
            btn.draw(screen, font)