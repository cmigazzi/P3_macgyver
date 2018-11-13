import pygame
from pygame.locals import *

from constants import *

class MapGame():
    """Represents the map"""
    def __init__(self):
        img_blue_wall = "graphics/blue_wall.png"
        self.blue_wall = pygame.image.load(img_blue_wall).convert()

    def display(self, screen):
        """Generates and diplays the map for the game
        
        Arguments:
            screen {pygame.Surface} -- The main screen
        """
        with open("map.txt") as file:
            map = file.read().split("\n")
            del map[-1]

        line_number = 0

        for line in map:
            for sprite in enumerate(line):
                x = sprite[0] * sprite_size
                y = line_number * sprite_size
                if sprite[1] == "W":
                    screen.blit(self.blue_wall, (x, y))
                if sprite[0] == 14:
                    line_number += 1


class MacGyver():
    """Represents the main character, MacGyver"""
    def __init__(self):
        img_macgyver = "graphics/MacGyver.png"
        self.image = pygame.image.load(img_macgyver).convert_alpha()

    def display(self, screen):
        with open("map.txt") as file:
            map = file.read().split("\n")
            del map[-1]

        line_number = 0

        for line in map:
            for sprite in enumerate(line):
                x = sprite[0] * sprite_size
                y = line_number * sprite_size
                if sprite[1] == "S":
                    screen.blit(self.image, (x, y))
                if sprite[0] == 14:
                    line_number += 1

    def move(self, direction):
        print("move")
        rect = self.image.get_rect()
        if direction == "RIGHT":
            print("right")
            new_position = position.move(3,0)
        
        return new_position

    def die(self):
        pass
    def win(self):
        pass
