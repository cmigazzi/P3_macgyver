import pygame
from pygame.locals import *

from constants import *

class MapGame():
    """Represents the map"""
    def __init__(self, wall_color):
        img_wall = walls[wall_color]
        self.wall = pygame.image.load(img_wall).convert()

    def display(self, screen, first=False):
        """Generates and diplays the map for the game
        
        Arguments:
            screen {pygame.Surface} -- The main screen
        """
        with open("map.txt") as file:
            map = file.read().split("\n")

        line_number = 0
        walls_positions = []
        path_positions = []

        for line in map:
            for sprite in enumerate(line):
                x = sprite[0] * sprite_size
                y = line_number * sprite_size
                if sprite[1] == "W":
                    wall_position = self.wall.get_rect(topleft=(x,y))
                    if first == True:
                        walls_positions.append(wall_position)
                    screen.blit(self.wall, wall_position)
                if sprite[1] == " ":
                    path_position = pygame.Rect(x,y,sprite_size,sprite_size)
                    if first == True:
                        path_positions.append(path_position)
                if sprite[0] == 14:
                    line_number += 1

        if first == True:
            self.walls_positions = walls_positions
            self.path_positions = path_positions    

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
        """Moves macgyver when directionnal keys are pressed
        
        Arguments:
            screen {pygame.Surface} -- The main screen
            direction {pygame.event.key} -- Which key is pressed
            walls_positions {list} -- Position of all the walls listed as pygame.Rect object
        """
        # absolute possible ways
        rect_right = pygame.Rect(self.position.left, self.position.top + sprite_size, sprite_size, sprite_size)
        rect_left = pygame.Rect(self.position.left, self.position.top - sprite_size, sprite_size, sprite_size)
        rect_up = pygame.Rect(self.position.left - sprite_size, self.position.top, sprite_size, sprite_size)
        rect_down = pygame.Rect(self.position.left + sprite_size, self.position.top, sprite_size, sprite_size)

        abs_possible_way = [rect_down, rect_up, rect_right, rect_left]
        impossible_ways = [w for w in walls_positions if w in abs_possible_way]

        if direction == K_RIGHT:
            new_position = self.position.move(sprite_size,0)
        if direction == K_LEFT:
            new_position = self.position.move(-sprite_size,0)
        if direction == K_DOWN:
            new_position = self.position.move(0,sprite_size)            
        if direction == K_UP:
            new_position = self.position.move(0,-sprite_size)

        if new_position not in impossible_ways and new_position.top >= 0 and new_position.left >= 0:
            self.position = new_position

        screen.blit(self.image, self.position)

    def die(self):
        pass
    def win(self):
        pass

class Guard():
    """Represents th guard"""
    def __init__(self):
        img_macgyver = "graphics/Gardien.png"
        self.image = pygame.image.load(img_macgyver).convert_alpha()

    def display(self, screen):
        """Displays guard on the map
        
        Arguments:
            screen {pygame.Surface} -- The main screen
        """
        with open("map.txt") as file:
            map = file.read().split("\n")

        line_number = 0

        for line in map:
            for sprite in enumerate(line):
                x = sprite[0] * sprite_size
                y = line_number * sprite_size
                if sprite[1] == "F":
                    self.position = self.image.get_rect(topleft=(x,y))
                    screen.blit(self.image, self.position)
                if sprite[0] == 14:
                    line_number += 1

class Object():
    """Represents an object on the map"""        
    def __init__(self, img_path):
        img_object = pygame.image.load(img_path).convert_alpha()
        self.image = img_object
        self.position = None
    
    def display(self, screen, position=None):
        if self.position == None:
            self.position = position

        screen.blit(self.image, self.position)

class Counter():
    def __init__(self, nb_items):
        self.nb_items = nb_items
        self.items_found = 0        
    
    def display(self, screen, items_found=0):


        font = pygame.font.SysFont("arial", 20, bold=True)
        text_list = ["ITEMS: ", str(items_found), "/", str(self.nb_items)]
        text = "".join(text_list)
        text = font.render(text, 1, (255,255,0))
        self.image = text
        

        position = self.image.get_rect(center=(300, 20))
        screen.blit(self.image, position)
