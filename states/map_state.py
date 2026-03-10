import pygame

class MapState:

    def __init__(self):
        self.map_area = pygame.Rect(20, 20, 650, 560)

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.map_area.collidepoint(event.pos):
                return "COMBAT"

    def update(self):
        pass

    def draw(self, screen, font):

        pygame.draw.rect(screen, (60,60,90), self.map_area)

        text = font.render("Click map to start combat", True, (255,255,255))
        screen.blit(text, (200,250))