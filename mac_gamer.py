import random

import pygame
from pygame.locals import *

from constants import *
from classes import MapGame, MacGyver, Guard, Object, Counter

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

    states = {
        "game": True,
        "menu": True,
        "play_game": False,
        "settings": False,
        "music": True,
        "wall_color": "blue"
    }   

    # sounds
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.load(music_intro)
    if states["music"] == True:    
        pygame.mixer.music.play(loops=-1)

    while states["game"] == True:

        screen.fill((0,0,0))
        screen.blit(intro, (100,100))
        screen.blit(title, title_pos)
        screen.blit(play, play_pos)
        screen.blit(settings, settings_pos)
        screen.blit(exit, exit_pos)     
        
        if states["menu"] == True:             
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
                        states["play_game"] = True
                        states["menu"] = False
                        
                    elif settings_pos.collidepoint(mouse_pos):
                        states["settings"] = True
                        states["menu"] = False

                    elif exit_pos.collidepoint(mouse_pos):
                        states["game"] = False      
        
        elif states["play_game"] == True:
            states = play_game(screen, states)
            if states["music"] == True:
                pygame.mixer.music.load(music_intro)    
                pygame.mixer.music.play(loops=-1)
        
        elif states["settings"] == True:
            states = settings_view(screen, states)

        if event.type == QUIT:
            states["game"] = False

        pygame.display.flip()

def play_game(screen, states):
    """
        This is the loop of the game
    """
    # Sounds
    item_sound = pygame.mixer.Sound(music_item)
    item_sound.set_volume(0.25)
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.load(music_play)
    if states["music"] == True:    
        pygame.mixer.music.play(loops=-1)

    background = pygame.image.load(img_background).convert()
    screen.blit(background, (0,0))
       
    map_game = MapGame(states["wall_color"])
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
    items_found = 0

    objects_positions = random.sample(paths_list, number_of_objects)

    objects_with_positions = list(zip(objects, objects_positions))

    for (obj, position) in objects_with_positions:
        obj.display(screen, position)

    counter = Counter(number_of_objects)
    counter.display(screen)

    while states["play_game"] == True:
                       
        for event in pygame.event.get():
            if event.type == QUIT:
                ending = False
                states["play_game"] = False
                states["game"] = False  

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_SPACE:
                    ending = False
                    states["play_game"] = False                    
                    states["menu"] = True      

                if states["play_game"] == True:   
                              

                    if event.key == K_RIGHT or K_LEFT or K_UP or K_DOWN:  
                        screen.blit(background, (0,0))
                        map_game.display(screen)
                        guard.display(screen)
                        for obj in objects:
                                    obj.display(screen)
                        counter.display(screen, items_found)                     
                        macgyver.move(screen, event.key, walls_list)              
                           
        
        if states["play_game"] == True:
            
            objects = [o for o in objects if not o.position.topleft == macgyver.position.topleft]

            prev_items_found = items_found
            items_found = number_of_objects - len(objects)
            if items_found != prev_items_found and states["music"] == True:
               item_sound.play()

            if guard.position == macgyver.position:
                states["play_game"] = False
                ending = True

        pygame.display.flip()

    if ending == True:
        if number_of_objects - items_found == 0 and states["music"] == True:
            pygame.mixer.music.load(music_win)  
            pygame.mixer.music.play()
        elif states["music"] == True:
            pygame.mixer.music.load(music_loose)  
            pygame.mixer.music.play()

        while ending == True:
            if number_of_objects - items_found == 0:
                result_font = pygame.font.SysFont("arial", 100, bold=True)
                comment_font = pygame.font.SysFont("arial", 32, bold=True)
                result = result_font.render("YOU WIN !!!!", 1, (0,0,0), (255,255,255))
                result_pos = result.get_rect(center=(300, 300))
                comment = comment_font.render("Press any key to return to menu", 1, (0,0,0), (255,255,255))
                comment_pos = comment.get_rect(center=(300, 450))
            
            else:         
                result_font = pygame.font.SysFont("arial", 87, bold=True)
                comment_font = pygame.font.SysFont("arial", 32, bold=True)
                result = result_font.render("YOU LOOSE...", 1, (255,255,255), (0,0,0))
                result_pos = result.get_rect(center=(300, 300))
                comment = comment_font.render("Press any key to return to menu", 1, (255,255,255), (0,0,0))
                comment_pos = comment.get_rect(center=(300, 450))
                


            screen.blit(background, (0,0))
            map_game.display(screen)
            screen.blit(result, result_pos)
            screen.blit(comment, comment_pos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    ending = False
                    states["game"] = False     

                if event.type == KEYDOWN: 
                    ending = False
                    states["menu"] = True

            pygame.display.flip()

    return states

def settings_view(screen, states):
    """
        This is the loop for the settings
    """
    #fonts
    settings_title_font = pygame.font.SysFont("arial", 24, bold=True)
    settings_text_font = pygame.font.SysFont("arial", 18, bold=True)
    #texts
    title_text = settings_title_font.render("S E T T T I N G S", 1, (255,255,255))
    title_text_pos = title_text.get_rect()
    title_text_pos.center = (300, 50)

    music_text = settings_text_font.render("MUSIC:", 1, (255,255,255))
    music_text_pos = music_text.get_rect()
    music_text_pos.center = (250, 180)

    on_off_text = settings_text_font.render("ON", 1, (255,255,255))
    on_off_pos = on_off_text.get_rect()
    on_off_pos.center = (350, 180)

    wall_color_text = settings_text_font.render("CHOOSE WALLS COLOR: ", 1, (255,255,255))
    wall_color_text_pos = wall_color_text.get_rect()
    wall_color_text_pos.center = (300, 250)

    menu_text = settings_text_font.render("RETURN TO MENU", 1, (255,255,255))
    menu_text_pos = menu_text.get_rect()
    menu_text_pos.center = (300, 400)

    #walls preview
    blue = pygame.image.load(walls["blue"]).convert()
    blue_pos = blue.get_rect()
    blue_pos.center = (220, 320)
    green = pygame.image.load(walls["green"]).convert()
    green_pos = green.get_rect()
    green_pos.center = (270, 320)
    red = pygame.image.load(walls["red"]).convert()
    red_pos = red.get_rect()
    red_pos.center = (320, 320)
    purple = pygame.image.load(walls["purple"]).convert() 
    purple_pos = purple.get_rect() 
    purple_pos.center = (370, 320)

    #border
    border = pygame.Surface((42,42))
    border.fill((255,255,255))
    blue_border_pos = border.get_rect()
    blue_border_pos.center = blue_pos.center
    green_border_pos = border.get_rect()
    green_border_pos.center = green_pos.center
    red_border_pos = border.get_rect()
    red_border_pos.center = red_pos.center
    purple_border_pos = border.get_rect()
    purple_border_pos.center = purple_pos.center
    
    is_border_active = {
       "blue": False,
       "green": False,
       "red": False,
       "purple": False,
    }

    while states["settings"] == True:
        if states["music"] == False:
            pygame.mixer.music.stop()

        screen.fill((0,0,0))        
        screen.blit(title_text, title_text_pos),
        screen.blit(music_text, music_text_pos)
        screen.blit(on_off_text, on_off_pos)
        screen.blit(wall_color_text, wall_color_text_pos)
        screen.blit(menu_text, menu_text_pos)

        if states["wall_color"] == "blue":
            screen.blit(border, blue_border_pos)
        if states["wall_color"] == "green":
            screen.blit(border, green_border_pos)
        if states["wall_color"] == "red":
            screen.blit(border, red_border_pos)
        if states["wall_color"] == "purple":
            screen.blit(border, purple_border_pos)

        if is_border_active["blue"] == True:
            screen.blit(border, blue_border_pos)
        if is_border_active["green"] == True:
            screen.blit(border, green_border_pos)
        if is_border_active["red"] == True:
            screen.blit(border, red_border_pos)
        if is_border_active["purple"] == True:
            screen.blit(border, purple_border_pos)

        screen.blit(blue, blue_pos)
        screen.blit(green, green_pos)
        screen.blit(purple, purple_pos)
        screen.blit(red, red_pos)       

        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                mouse_pos = event.pos
                if blue_pos.collidepoint(mouse_pos):
                    is_border_active = {
                            "blue": True,
                            "green": False,
                            "red": False,
                            "purple": False,
                        }
                
                elif green_pos.collidepoint(mouse_pos):
                    is_border_active = {
                            "blue": False,
                            "green": True,
                            "red": False,
                            "purple": False,
                        }

                elif red_pos.collidepoint(mouse_pos):
                    is_border_active = {
                            "blue": False,
                            "green": False,
                            "red": True,
                            "purple": False,
                        }
                
                elif purple_pos.collidepoint(mouse_pos):
                    is_border_active = {
                            "blue": False,
                            "green": False,
                            "red": False,
                            "purple": True,
                        }
                elif menu_text_pos.collidepoint(mouse_pos):
                    menu_text = settings_text_font.render("RETURN TO MENU", 1, (255,255,0))
                
                elif on_off_pos.collidepoint(mouse_pos):
                    if states["music"] == True:
                            on_or_off = "ON"
                    else:
                        on_or_off = "OFF"
                    on_off_text = settings_text_font.render(on_or_off, 1, (255,255,0))

                else:
                    menu_text = settings_text_font.render("RETURN TO MENU", 1, (255,255,255))
                    if states["music"] == True:
                            on_or_off = "ON"
                    else:
                        on_or_off = "OFF"
                    on_off_text = settings_text_font.render(on_or_off, 1, (255,255,255))

                    is_border_active = {
                        "blue": False,
                        "green": False,
                        "red": False,
                        "purple": False,
                        }

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos   
                    if blue_pos.collidepoint(mouse_pos):
                         states["wall_color"] = "blue"

                    if green_pos.collidepoint(mouse_pos):
                        states["wall_color"] = "green" 
                    
                    if red_pos.collidepoint(mouse_pos):
                        states["wall_color"] = "red"                   
                
                    if purple_pos.collidepoint(mouse_pos):
                        states["wall_color"] = "purple"

                    if on_off_pos.collidepoint(mouse_pos):
                        states["music"] = not states["music"] 
                        if states["music"] == True:
                            on_or_off = "ON"
                        else:
                            on_or_off = "OFF"

                        on_off_text = settings_text_font.render(on_or_off, 1, (255,255,255))
                        
                    
                    if menu_text_pos.collidepoint(mouse_pos):
                        states["settings"] = False
                        states["menu"] = True 
                    
                    
                    
            if event.type == QUIT:
                states["settings"] = False
                states["play_game"] = False
                states["game"] = False
        
        pygame.display.flip()

    return states

if __name__ == "__main__":
    main()
