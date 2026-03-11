import pygame

ICON_SIZE = 28

mob_icon = None
event_icon = None
shop_icon = None
elite_icon = None
rest_icon = None
boss_icon = None


def load_icons():

    global mob_icon, event_icon, shop_icon, elite_icon, rest_icon, boss_icon

    mob_icon = pygame.image.load("assets/icons/mob.png").convert_alpha()
    event_icon = pygame.image.load("assets/icons/event.png").convert_alpha()
    shop_icon = pygame.image.load("assets/icons/shop.png").convert_alpha()
    elite_icon = pygame.image.load("assets/icons/elite.png").convert_alpha()
    rest_icon = pygame.image.load("assets/icons/rest.png").convert_alpha()
    boss_icon = pygame.image.load("assets/icons/boss.png").convert_alpha()

    # resize icons
    mob_icon = pygame.transform.scale(mob_icon,(ICON_SIZE,ICON_SIZE))
    event_icon = pygame.transform.scale(event_icon,(ICON_SIZE,ICON_SIZE))
    shop_icon = pygame.transform.scale(shop_icon,(ICON_SIZE,ICON_SIZE))
    elite_icon = pygame.transform.scale(elite_icon,(ICON_SIZE,ICON_SIZE))
    rest_icon = pygame.transform.scale(rest_icon,(ICON_SIZE,ICON_SIZE))
    boss_icon = pygame.transform.scale(boss_icon,(ICON_SIZE,ICON_SIZE))




class MapNode:

    def __init__(self, x, y, node_type):

        self.x = x
        self.y = y

        self.type = node_type

        self.radius = 18

        self.connections = []

        self.visited = False


    def clicked(self, pos):

        dx = pos[0] - self.x
        dy = pos[1] - self.y

        return dx*dx + dy*dy <= self.radius*self.radius


    def draw(self, screen, font, available=False):

        # cor base
        color = (200,200,200)

        if self.type == "mob":
            color = (200,80,80)

        elif self.type == "event":
            color = (80,200,200)

        elif self.type == "elite":
            color = (200,100,200)

        elif self.type == "start":
            color = (200,200,200)

        # node base
        pygame.draw.circle(screen, color, (self.x,self.y), self.radius)

        # highlight se visitado
        if self.visited:
            pygame.draw.circle(screen, (255,255,0), (self.x,self.y), self.radius+8, 2)

        # highlight se disponível
        if available:
            pygame.draw.circle(screen, (255,255,255), (self.x,self.y), self.radius+6, 2)




        # ícones
        icon = None

        if self.type == "mob":
            icon = mob_icon

        elif self.type == "event":
            icon = event_icon

        elif self.type == "shop":
            icon = shop_icon

        elif self.type == "elite":
            icon = elite_icon

        elif self.type == "rest":
            icon = rest_icon

        elif self.type == "boss":
            icon = boss_icon

        if icon:
            rect = icon.get_rect(center=(self.x,self.y))
            screen.blit(icon, rect)


