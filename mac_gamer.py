import pygame
from pygame.locals import *

from constants import *

def main():
    """
        This is the main loop of the game, it provides the menu of the game
    """
    pygame.display.init()
    pygame.font.init()
    pygame.mixer.init()

    # screen init
    screen = pygame.display.set_mode((screen_size, screen_size))

    # intro elements
    intro = pygame.image.load(img_intro).convert()
    title_font = pygame.font.SysFont("arial", 24, bold=True)
    menu_font = pygame.font.SysFont("arial", 18, bold=True)
    pygame.mixer.music.load(music_intro)

    title = title_font.render("M A C G A M E R", 1, (255,255,255))
    title_pos = title.get_rect()
    title_pos.center = (300, 50)

    # Menu buttons
    play = menu_font.render("PLAY", 1, (255,255,255))
    play_pos = play.get_rect(center=(150,550))

    settings = menu_font.render("SETTINGS", 1, (255,255,255))
    settings_pos = settings.get_rect(center=(300, 550))

    exit = menu_font.render("QUIT", 1, (255,255,255))
    exit_pos = exit.get_rect(center=(450,550))


    game = True
    pygame.mixer.music.play(loops=-1)

    while game == True:
        screen.blit(intro, (100,100))
        screen.blit(title, title_pos)
        screen.blit(play, play_pos)
        screen.blit(settings, settings_pos)
        screen.blit(exit, exit_pos)

        for event in pygame.event.get():

            if event.type == MOUSEMOTION:
                mouse_pos = event.pos
                if play_pos.collidepoint(mouse_pos):
                    play = menu_font.render("PLAY", 1, (255,255,0))
                elif settings_pos.collidepoint(mouse_pos):
                    settings = menu_font.render("SETTINGS", 1, (255,255, 0))
                elif exit_pos.collidepoint(mouse_pos):
                    exit = menu_font.render("QUIT", 1, (255,255,0))
                else:
                    play = menu_font.render("PLAY", 1, (255,255,255))
                    settings = menu_font.render("SETTINGS", 1, (255,255,255))
                    exit = menu_font.render("QUIT", 1, (255,255,255)) 
                 
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if play_pos.collidepoint(mouse_pos):
                    game = play_game(screen)
                elif settings_pos.collidepoint(mouse_pos):
                    print("settings")
                elif exit_pos.collidepoint(mouse_pos):
                    game = False                       

            if event.type == QUIT:
                game = False

        pygame.display.flip()

def play_game(screen):
    """
        This is the loop of the game
    """
    play = True
    while play == True:
        background = pygame.image.load(img_background).convert()
        wall = pygame.image.load(img_blue_wall).convert()

        screen.blit(background, (0,0))

        with open("map.txt") as file:
            map = file.read().split("\n")
            del map[-1]

        line_number = 0

        for line in map:
            for sprite in enumerate(line):
                x = sprite[0] * sprite_size
                y = line_number * sprite_size
                if sprite[1] == "W":
                    screen.blit(wall, (x, y))
                if sprite[0] == 14:
                    line_number += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            
        pygame.display.flip()


def settings():
    """
        This is the loop for the settings
    """
    pass



if __name__ == "__main__":
    main()
