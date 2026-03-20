import pygame

class DamageText:

    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.timer = 50   # duração

    def update(self):
        self.y -= 1
        self.timer -= 1

    def draw(self, screen, font):
        self.update()   
        img = font.render(self.text, True, self.color)
        screen.blit(img, (self.x, self.y))

    def alive(self):
        return self.timer > 0