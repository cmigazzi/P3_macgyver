import random

import pygame
from pygame.locals import *

from constants import *
from classes import MapGame, MacGyver, Guard, Object

def main():
    """
        This is the main loop of the app, it displays the menu of the game
    """
    pygame.display.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.key.set_repeat(400, 30)

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

    #pygame.mixer.music.play(loops=-1)

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
    background = pygame.image.load(img_background).convert()
    screen.blit(background, (0,0))
       
    map_game = MapGame()
    map_game.display(screen, first=True)
    #Get walls and path coordonates
    walls_list = map_game.walls_positions
    paths_list = map_game.path_positions

    macgyver = MacGyver()
    macgyver.display(screen)

    guard = Guard()
    guard.display(screen)

    objects = [Object(img_obj_1), 
               Object(img_obj_2),
               Object(img_obj_1),
               Object(img_obj_2)]

    number_of_objects = len(objects)

    objects_positions = random.sample(paths_list, number_of_objects)

    objects_with_positions = list(zip(objects, objects_positions))

    for (obj, position) in objects_with_positions:
        obj.display(screen, position)

    play = True
    while play == True:               
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                screen.blit(background, (0,0))
                map_game.display(screen)
                guard.display(screen)
                for obj in objects:
                    obj.display(screen)
                if event.key == K_RIGHT or K_LEFT or K_UP or K_DOWN:                    
                    macgyver.move(screen, event.key, walls_list)
                if event.key == K_ESCAPE or event.key == K_SPACE:
                    return False

            if event.type == QUIT:
                return False        
        
        for obj in objects:
            if macgyver.position == obj.position:
                del obj

        if guard.position == macgyver.position:
            play = False
            ending = True
        pygame.display.flip()

    while ending == True:
        win_font = pygame.font.SysFont("arial", 100, bold=True)
        comment_font = pygame.font.SysFont("arial", 32, bold=True)
        win = win_font.render("YOU WIN !!!!", 1, (0,0,0), (255,255,255))
        win_pos = win.get_rect(center=(300, 300))
        comment = comment_font.render("Press any key to return to menu", 1, (0,0,0), (255,255,255))
        comment_pos = comment.get_rect(center=(300, 450))

        screen.blit(background, (0,0))
        map_game.display(screen)
        screen.blit(win, win_pos)
        screen.blit(comment, comment_pos)

        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN:
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
