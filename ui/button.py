import pygame


class Button:

    def __init__(self, x, y, width, height, text):

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

        self.color = (150,60,60)
        self.hover_color = (180,80,80)

    def draw(self, screen, font):

        mouse = pygame.mouse.get_pos()

        color = self.color

        if self.rect.collidepoint(mouse):
            color = self.hover_color

        pygame.draw.rect(screen, color, self.rect)

        label = font.render(self.text, True, (255,255,255))
        screen.blit(
            label,
            (
                self.rect.x + self.rect.width//2 - label.get_width()//2,
                self.rect.y + self.rect.height//2 - label.get_height()//2
            )
        )

    def clicked(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                return True

        return False