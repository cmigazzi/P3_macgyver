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
        """Displays macgyver on the map
        
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
                if sprite[1] == "S":
                    self.position = self.image.get_rect(topleft=(x,y))
                    screen.blit(self.image, self.position)
                if sprite[0] == 14:
                    line_number += 1        

    def move(self, screen, direction):
        print(self.position)
        if direction == K_RIGHT:
            self.position = self.position.move(3,0)
        if direction == K_LEFT:
            self.position = self.position.move(-3,0)
        if direction == K_DOWN:
            self.position = self.position.move(0,3)
        if direction == K_UP:
            self.position = self.position.move(0,-3)       
        
        screen.blit(self.image, self.position)

    def die(self):
        pass
    def win(self):
        pass
