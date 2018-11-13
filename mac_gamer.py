import pygame
from pygame.locals import *

from constants import *

def main():
    """
        This is the main loop of the app, it displays the menu of the game
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
    pygame.mixer.music.set_volume(0.2)

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
    menu_state = True
    play_game_state = False
    settings_state = False

    pygame.mixer.music.play(loops=-1)

    while game == True:
        screen.fill((0,0,0))
        screen.blit(intro, (100,100))
        screen.blit(title, title_pos)
        screen.blit(play, play_pos)
        screen.blit(settings, settings_pos)
        screen.blit(exit, exit_pos)        
        
        if menu_state == True:
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
                        play_game_state = True
                        menu_state = False
                    elif settings_pos.collidepoint(mouse_pos):
                        settings_state = True
                        menu_state = False
                    elif exit_pos.collidepoint(mouse_pos):
                        game = False
        
        elif play_game_state == True:
            play_game_state = play_game(screen)
            menu_state = True
        
        elif settings_state == True:
            settings_state = settings_view(screen)
            menu_state = True
                
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
        guard = pygame.image.load(img_guard).convert_alpha()

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
                if sprite[1] == "F":
                    screen.blit(guard, (x, y))
                if sprite[0] == 14:
                    line_number += 1

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_SPACE:
                    return False

            if event.type == QUIT:
                return False
               
            
        pygame.display.flip()


def settings_view(screen):
    """
        This is the loop for the settings
    """
    settings = True
    settings_title_font = pygame.font.SysFont("arial", 24, bold=True)
    settings_title = settings_title_font.render("""SETTTINGS WILL BE THERE SOON""", 1, (255,255,255))
    settings_title_pos = settings_title.get_rect()
    settings_title_pos.center = (300, 50)

    while settings == True:
        screen.fill((0,0,0))
        screen.blit(settings_title, settings_title_pos)

        for event in pygame.event.get():
            if event.type == QUIT:
                return False
        
        pygame.display.flip()
        



if __name__ == "__main__":
    main()
