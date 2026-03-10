import pygame

class DamageText:

    def __init__(self, x, y, text, color):

        self.x = x
        self.y = y

        self.text = text
        self.color = color

        self.timer = 60
        self.velocity = -1

    def update(self):

        self.y += self.velocity
        self.timer -= 1

    def draw(self, screen, font):

        alpha = int(255 * (self.timer / 60))

        text_surface = font.render(self.text, True, self.color)
        text_surface.set_alpha(alpha)

        screen.blit(text_surface, (self.x, self.y))

    def alive(self):

        return self.timer > 0