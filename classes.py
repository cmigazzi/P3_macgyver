import pygame
from pygame.locals import *

from constants import *

class MapGame():
    """Represents the map"""
    def __init__(self):
        img_wall = "graphics/blue_wall.png"
        self.wall = pygame.image.load(img_wall).convert()

    def display(self, screen):
        """Generates and diplays the map for the game
        
        Arguments:
            screen {pygame.Surface} -- The main screen
        """
        with open("map.txt") as file:
            map = file.read().split("\n")
            del map[-1]

        line_number = 0
        walls_positions = []

        for line in map:
            for sprite in enumerate(line):
                x = sprite[0] * sprite_size
                y = line_number * sprite_size
                if sprite[1] == "W":
                    wall_position = self.wall.get_rect(topleft=(x,y))
                    walls_positions.append(wall_position)
                    screen.blit(self.wall, wall_position)
                if sprite[0] == 14:
                    line_number += 1

        self.walls_positions = walls_positions
        


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

    def move(self, screen, direction, walls_positions):
        rect_right = pygame.Rect(self.position.left, self.position.top + sprite_size, sprite_size, sprite_size)
        rect_left = pygame.Rect(self.position.left, self.position.top - sprite_size, sprite_size, sprite_size)
        rect_up = pygame.Rect(self.position.left - sprite_size, self.position.top, sprite_size, sprite_size)
        rect_down = pygame.Rect(self.position.left + sprite_size, self.position.top, sprite_size, sprite_size)

        print("position:", self.position)
        abs_possible_way = [rect_down, rect_up, rect_right, rect_left]
        print("Possible:", abs_possible_way)
        impossible_ways = [w for w in walls_positions if w in abs_possible_way]
        print("impossible:", impossible_ways)

        if direction == K_RIGHT:
            new_position = self.position.move(sprite_size,0)

        if direction == K_LEFT:
            new_position = self.position.move(-sprite_size,0)
        
        if direction == K_DOWN:
            new_position = self.position.move(0,sprite_size)
            
        if direction == K_UP:
            new_position = self.position.move(0,-sprite_size)
        
        if new_position not in impossible_ways:
            self.position = new_position

        screen.blit(self.image, self.position)

    def die(self):
        pass
    def win(self):
        pass
