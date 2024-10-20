import pygame
import random
import math

pygame.init()

infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

class Sky:
    def __init__(self, sky_no):
        self.sky_no = sky_no
        if self.sky_no == 0:
            self.dark_blue =  (92,49,163) # (92,49,163)
            self.dark_purple = (222,121,30)  # used to be (92,49,163)
            self.black = (234,90,111)
        elif self.sky_no == 1:
            self.dark_blue =  (70, 113, 226) # (92,49,163)
            self.dark_purple = (60, 0, 100)  # used to be (92,49,163)
            self.black = (0, 0, 0)
        elif self.sky_no == 2:
            self.dark_blue = (131,35,136)
            self.dark_purple = (227,67,107)
            self.black = (119,47,240)
            

        # Generate 100 colors for the transition
        self.colors = [
            (
                self.dark_blue[0] + (self.dark_purple[0] - self.dark_blue[0]) * i // 200,
                self.dark_blue[1] + (self.dark_purple[1] - self.dark_blue[1]) * i // 200,
                self.dark_blue[2] + (self.dark_purple[2] - self.dark_blue[2]) * i // 200
            )
            for i in range(200)
        ] + [
            (
                self.dark_purple[0] + (self.black[0] - self.dark_purple[0]) * i // 200,
                self.dark_purple[1] + (self.black[1] - self.dark_purple[1]) * i // 200,
                self.dark_purple[2] + (self.black[2] - self.dark_purple[2]) * i // 200
            )
            for i in range(200)
        ]

        self.layer_heights = [HEIGHT // len(self.colors) + (1 if i < HEIGHT % len(self.colors) else 0) for i in range(len(self.colors))]
        self.layers = []

        for color, layer_height in zip(self.colors, self.layer_heights):
            surface = pygame.Surface((WIDTH, layer_height))
            surface.fill(color)
            self.layers.append(surface)

        self.layers.reverse()
        
        self.star_num = 150
        self.x_list = []
        self.y_list = []
        for i in range(self.star_num):
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT - 600)
            self.x_list.append(self.x)
            self.y_list.append(self.y)
        

    def draw_star(self, x, y, size):
        outer_points = []
        inner_points = []
        angle_offset = math.pi / 4 # Offset to create a four-pointed star

        for i in range(5):
            outer_x = x + size * math.cos(angle_offset + i * (2 * math.pi / 5))
            outer_y = y + size * math.sin(angle_offset + i * (2 * math.pi / 5))
            outer_points.append((outer_x, outer_y))

            inner_x = x + (size // 2) * math.cos(angle_offset + (i + 0.5) * (2 * math.pi / 5))
            inner_y = y + (size // 2) * math.sin(angle_offset + (i + 0.5) * (2 * math.pi / 5))
            inner_points.append((inner_x, inner_y))

        pygame.draw.polygon(WIN, (255, 255, 255), inner_points)

    def draw_stars(self, num_stars):
        for i in range(num_stars):
            if i % 15 == 0 or i == 0:
                size = random.randint(5, 10)
            self.draw_star(self.x_list[i], self.y_list[i], size)

    def sky_gen(self):
        y = 0  # Start from the top of the window
        for layer in self.layers:
            WIN.blit(layer, (0, y))
            y += layer.get_height()
        self.draw_stars(self.star_num)  # Adjust the number of stars as needed

    def update_stars_position(self, player_speed, player_facing):
        for i in range(self.star_num):
            if player_facing:
                self.x_list[i] -= player_speed
                if self.x_list[i] < 0:
                    self.x_list[i] = WIDTH
            else:
                self.x_list[i] += player_speed
                if self.x_list[i] > WIDTH:
                    self.x_list[i] = 0
