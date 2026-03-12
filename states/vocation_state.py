import pygame
from ui.button import Button


class VocationSelect:

    def __init__(self):

        self.buttons = []

        self.classes = [
            ("Warrior", "warrior"),
            ("Hunter", "hunter"),
            ("Mage", "mage")
        ]

        start_y = 250

        for i, cls in enumerate(self.classes):

            btn = Button(
                350,
                start_y + i * 80,
                300,
                60,
                cls[0]
            )

            self.buttons.append(btn)


    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            for i, button in enumerate(self.buttons):

                if button.clicked(event):

                    vocation = self.classes[i][1]

                    return ("START_GAME", vocation)


    def update(self):
        pass


    def draw(self, screen, font):

        title_font = pygame.font.SysFont(None, 60)

        title = title_font.render("Choose Your Class", True, (255,255,255))

        screen.blit(title, (320,150))

        for button in self.buttons:
            button.draw(screen, font)