import pygame
import random

from ui.button import Button
from items.items import items


class ShopState:

    def __init__(self, player):

        self.player = player

        # preços
        self.str_price = 40
        self.mgc_price = 40
        self.heal_price = 30
        self.item_price = 60

        # layout
        start_y = 220
        gap = 70

        line = 0

        # ========================
        # STR
        # ========================

        self.str_button = Button(
            300,
            start_y + line * gap,
            300,
            50,
            f"+1 STR ({self.str_price}g)"
        )
        line += 1


        # ========================
        # MGC
        # ========================

        self.mgc_button = Button(
            300,
            start_y + line * gap,
            300,
            50,
            f"+1 MGC ({self.mgc_price}g)"
        )
        line += 1


        # ========================
        # HEAL
        # ========================

        self.heal_button = Button(
            300,
            start_y + line * gap,
            300,
            50,
            f"Heal Full HP ({self.heal_price}g)"
        )
        line += 1


        # ========================
        # RANDOM ITEM
        # ========================

        self.item_button = Button(
            300,
            start_y + line * gap,
            300,
            50,
            f"Random Item ({self.item_price}g)"
        )
        line += 1


        # ========================
        # LEAVE
        # ========================

        self.leave_button = Button(
            300,
            start_y + line * gap,
            300,
            50,
            "Leave"
        )


    # ========================
    # HANDLE INPUT
    # ========================

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:


            # ========================
            # STR
            # ========================

            if self.str_button.clicked(event):

                if self.player.gold >= self.str_price:

                    self.player.gold -= self.str_price
                    self.player.str += 1


            # ========================
            # MGC
            # ========================

            elif self.mgc_button.clicked(event):

                if self.player.gold >= self.mgc_price:

                    self.player.gold -= self.mgc_price
                    self.player.mgc += 1


            # ========================
            # HEAL
            # ========================

            elif self.heal_button.clicked(event):

                if self.player.gold >= self.heal_price:

                    self.player.gold -= self.heal_price
                    self.player.hp = self.player.max_hp


            # ========================
            # RANDOM ITEM
            # ========================

            elif self.item_button.clicked(event):

                if self.player.gold >= self.item_price:

                    self.player.gold -= self.item_price

                    item = random.choice(items)

                    self.player.items.append(item)

                    effect = item["effect"]
                    value = item["value"]

                    if effect == "str":
                        self.player.str += value

                    elif effect == "mgc":
                        self.player.mgc += value

                    elif effect == "block":
                        self.player.block += value


            # ========================
            # LEAVE
            # ========================

            elif self.leave_button.clicked(event):

                return "MAP"


    def update(self):
        pass


    # ========================
    # DRAW
    # ========================

    def draw(self, screen, font):

        title = font.render("Shop", True, (255,255,0))
        screen.blit(title, (380, 150))

        gold_text = font.render(f"Gold: {self.player.gold}", True, (255,215,0))
        screen.blit(gold_text, (380, 180))


        self.str_button.draw(screen, font)
        self.mgc_button.draw(screen, font)
        self.heal_button.draw(screen, font)
        self.item_button.draw(screen, font)

        self.leave_button.draw(screen, font)