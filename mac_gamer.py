import pygame
from pygame.locals import *

from constants import *

pygame.display.init()
pygame.font.init()
pygame.mixer.init()


# screen init
screen = pygame.display.set_mode((screen_size, screen_size))

# intro elements
intro = pygame.image.load(img_intro).convert()
title_font = pygame.font.SysFont("arial", 24, bold=True)
menu_font = pygame.font.SysFont("arial", 18, bold=True)
intro_sound = pygame.mixer.music.load(music_intro)

title = title_font.render("M A C G A M E R", 1, (255,255,255))
title_pos = title.get_rect()
title_pos.center = (300, 50)

menu = pygame.Surface((600, 100))
play = menu_font.render("PLAY", 1, (255,255,255))
play_pos = play.get_rect()
play_pos.center = (150, 50)
settings = menu_font.render("SETTINGS", 1, (255,255,255))
settings_pos = settings.get_rect()
settings_pos.center = (300, 50)
exit = menu_font.render("QUIT", 1, (255,255,255))
exit_pos = exit.get_rect()
exit_pos.center = (450, 50)


game = True
pygame.mixer.music.play(loops=-1)

while game == True:
    screen.blit(intro, (100,100))
    screen.blit(title, title_pos)
    screen.blit(menu, (0, 500))
    menu.blit(play, play_pos)
    menu.blit(settings, settings_pos)
    menu.blit(exit, exit_pos)

    for event in pygame.event.get():

        if event.type == QUIT:
            game = False

    pygame.display.flip()
