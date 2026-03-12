import pygame

class GameOverState:

    def __init__(self, player):
        self.player = player

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return "RESTART"

    def update(self):
        pass

    def draw(self, screen, font):

        w, h = screen.get_size()

        text = font.render("GAME OVER", True, (220,60,60))
        restart = font.render("Press R to restart run", True, (255,255,255))

        screen.blit(text, (w//2 - 60, h//2 - 20))
        screen.blit(restart, (w//2 - 110, h//2 + 20))
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))