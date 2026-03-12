import pygame
import random

from entities.map_node import MapNode


class MapState:

    def __init__(self):

        self.nodes = []
        self.node_lookup = {}
        self.rows = []

        width = 700
        height = 600

        cols = 7
        floors = 9
        paths = 4

        grid_x = width // (cols + 1)
        grid_y = height // (floors + 2)

        start_col = cols // 2
        start_x = grid_x * (start_col + 1)
        start_y = height - grid_y

        # START NODE
        start = MapNode(start_x, start_y, "start")

        self.nodes.append(start)
        self.node_lookup[(start_col, 0)] = start

        self.rows.append([start])

        # GENERATE PATHS
        for p in range(paths):

            col = start_col + random.choice([-1, 0, 1])
            prev_node = start

            for floor in range(1, floors):

                col += random.choice([-1, 0, 1])
                col = max(0, min(cols - 1, col))

                key = (col, floor)

                if key not in self.node_lookup:

                    x = grid_x * (col + 1)
                    y = start_y - floor * grid_y

                    node_type = random.choices(
                        ["mob","event","shop","rest","elite"],
                        weights=[50,25,10,10,5]
                    )[0]

                    node = MapNode(x, y, node_type)

                    self.node_lookup[key] = node
                    self.nodes.append(node)

                    while len(self.rows) <= floor:
                        self.rows.append([])

                    self.rows[floor].append(node)


                node = self.node_lookup[key]


                if node not in prev_node.connections:
                    if prev_node.x < node.x:
                        prev_node.connections.append(node)
                    elif prev_node.x > node.x:
                        prev_node.connections.append(node)
                    else:
                        prev_node.connections.append(node)



                prev_node = node

        # BOSS NODE
        boss_y = start_y - floors * grid_y
        boss_x = width // 2

        boss = MapNode(boss_x,boss_y,"boss")

        self.nodes.append(boss)

        for node in self.rows[-1]:
            node.connections.append(boss)

        self.rows.append([boss])

        # PLAYER START
        self.current_node = start
        start.visited = True


    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            for node in self.current_node.connections:

                if node.clicked(event.pos):

                    self.current_node = node
                    node.visited = True

                    if node.type in "mob":
                        return ("COMBAT", 1)
                    elif node.type in "elite":
                        return ("COMBAT", 2)
                    elif node.type in "boss":
                        return ("COMBAT", 4)
                    elif node.type in "rest":
                        return "REST"
                    elif node.type == "shop":
                        return "SHOP"


    def update(self):
        pass


    def draw(self, screen, font):

        # DRAW CONNECTIONS
        for node in self.nodes:

            for target in node.connections:

                pygame.draw.line(
                    screen,
                    (150,150,150),
                    (node.x,node.y),
                    (target.x,target.y),
                    3
                )

        # DRAW NODES
        for node in self.nodes:

            available = node in self.current_node.connections

            node.draw(screen, font, available)