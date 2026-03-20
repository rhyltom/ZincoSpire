import pygame
import random

from items.items import items
from ui.button import Button


class RewardState:

    def __init__(self, player, data):


        self.player = player

        self.type = data.get("type")
        t = data.get("type")

        # definir rewards
        if t == "mob":
            self.rewards = [
                {"name": "Heal 10 HP", "type": "heal"},
                {"name": "Gain 20 Gold", "type": "gold"}
        ]

        elif t == "elite":
            self.rewards = random.sample(items, 2)

        elif t == "boss":
            self.rewards = random.sample(items, 3)



        # criar botões
        self.buttons = []

        start_y = 260

        for i, reward in enumerate(self.rewards):

            btn = Button(
                300,
                start_y + i * 70,
                250,
                50,
                reward["name"]
            )

            self.buttons.append(btn)


    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            for i, button in enumerate(self.buttons):

                if button.clicked(event):

                    reward = self.rewards[i]

                    # reward de item
                    if self.type == "elite" or self.type == "boss":

                        self.player.items.append(reward)
                        self.apply_item_effect(reward)

                    # reward normal
                    else:

                        self.apply_reward(reward)

                    return "MAP"


    def apply_reward(self, reward):

        if reward["type"] == "heal":

            self.player.hp = min(
                self.player.hp + 10,
                self.player.max_hp
            )

        elif reward["type"] == "gold":

            self.player.gold += 20


    def apply_item_effect(self, item):

        effect = item["effect"]
        value = item["value"]

        if effect == "str":

            self.player.str += value

        elif effect == "mgc":

            self.player.mgc += value

        elif effect == "block":

            self.player.block += value


    def update(self):
        pass


    def draw(self, screen, font):

        # fundo da reward box
        pygame.draw.rect(screen, (70,70,70), (250,180,350,300))
        pygame.draw.rect(screen, (200,200,200), (250,180,350,300), 2)

        # título
        if self.type == "elite" or self.type == "boss":
            title_text = "Choose Item"
        else:
            title_text = "Choose Reward"

        title = font.render(title_text, True, (255,255,255))
        screen.blit(title, (340,200))


        # stats do player
        stats = font.render(
            f"HP {self.player.hp}/{self.player.max_hp} | STR {self.player.str} | MGC {self.player.mgc}",
            True,
            (200,200,200)
        )

        screen.blit(stats, (280,230))


        # desenhar botões
        for button in self.buttons:
            button.draw(screen, font)


        # descrição + icon dos items (elite)
        if self.type == "elite" or self.type == "boss":
            for i, reward in enumerate(self.rewards):

                y = 260 + i * 70
                # icon
                try:
                    icon = pygame.image.load(
                        f"items/{reward['icon']}"
                    ).convert_alpha()
                    icon = pygame.transform.scale(icon,(32,32))
                    screen.blit(icon,(260,y))

                except:
                    pygame.draw.rect(screen,(200,200,200),(260,y,32,32))


                # descrição
                desc = font.render(
                    reward["desc"],
                    True,
                    (200,200,200)
                )
                screen.blit(desc,(300,y+30))