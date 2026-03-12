import pygame
from ui.button import Button


CLASS_INFO = {

    "warrior": {
        "name": "Warrior",
        "desc": "Feral Berserk Fighter",
        "hp": 60,
        "str": 2,
        "mgc": 0,
        "skills": ["Power Strike", "Shield Block"]
    },

    "hunter": {
        "name": "Hunter",
        "desc": "Church's Royal Hunter",
        "hp": 50,
        "str": 1,
        "mgc": 0,
        "skills": ["Power Shot", "Evade"]
    },

    "mage": {
        "name": "Mage",
        "desc": "Arcane Spellcaster",
        "hp": 40,
        "str": 0,
        "mgc": 2,
        "skills": ["Fireball", "Mana Shield"]
    }
}


SCREEN_WIDTH = 1000
PANEL_WIDTH = 280

COMBAT_WIDTH = SCREEN_WIDTH - PANEL_WIDTH
COMBAT_CENTER_X = COMBAT_WIDTH // 2


class VocationSelect:

    def __init__(self):

        self.selected_class = None

        self.classes = [
            ("Warrior", "warrior"),
            ("Hunter", "hunter"),
            ("Mage", "mage")
        ]

        self.buttons = []

        start_y = 250
        button_width = 300

        for i, cls in enumerate(self.classes):

            btn = Button(
                COMBAT_CENTER_X - button_width // 2,
                start_y + i * 80,
                button_width,
                60,
                cls[0]
            )

            self.buttons.append(btn)

        # Confirm button (fora do loop!)
        self.confirm_button = Button(
            770,
            520,
            180,
            50,
            "Confirm"
        )


    # ========================
    # INPUT
    # ========================

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            for i, button in enumerate(self.buttons):

                if button.clicked(event):
                    self.selected_class = self.classes[i][1]

            if self.selected_class and self.confirm_button.clicked(event):

                return ("START_GAME", self.selected_class)


    def update(self):
        pass


    # ========================
    # DRAW
    # ========================

    def draw(self, screen, font):

        title_font = pygame.font.SysFont(None, 60)

        title = title_font.render("Choose Your Class", True, (255,255,255))
        title_rect = title.get_rect(center=(COMBAT_CENTER_X,150))

        screen.blit(title, title_rect)

        # draw class buttons
        for i, button in enumerate(self.buttons):

            cls = self.classes[i][1]

            # highlight selected class
            if self.selected_class == cls:
                pygame.draw.rect(screen, (180,80,60), button.rect)

            button.draw(screen, font)


        # ========================
        # RIGHT PANEL INFO
        # ========================

        if self.selected_class:

            info = CLASS_INFO[self.selected_class]

            x = 740
            y = 60

            name = font.render(info["name"], True, (255,255,255))
            screen.blit(name, (x,y))

            y += 40

            desc = font.render(info["desc"], True, (200,200,200))
            screen.blit(desc, (x,y))

            y += 60

            stats = font.render("Stats", True, (255,255,255))
            screen.blit(stats, (x,y))

            y += 30

            hp = font.render(f"HP: {info['hp']}", True, (200,200,200))
            screen.blit(hp, (x,y))

            y += 25

            strength = font.render(f"STR: {info['str']}", True, (200,200,200))
            screen.blit(strength, (x,y))

            y += 25

            magic = font.render(f"MGC: {info['mgc']}", True, (200,200,200))
            screen.blit(magic, (x,y))

            y += 40

            skills = font.render("Skills", True, (255,255,255))
            screen.blit(skills, (x,y))

            y += 30

            for skill in info["skills"]:

                skill_text = font.render(skill, True, (200,200,200))
                screen.blit(skill_text, (x,y))

                y += 25

            # draw confirm button
            self.confirm_button.draw(screen, font)