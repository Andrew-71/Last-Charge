# Scenario:
# Daniel, a domestic android learned that its owners wanted to replace it,
# and after something happened with its software it suddenly attacked them,
# taking a 9 years old girl hostage and killing her father together with 3 responding policemen in the process.
# a prototype android Connor is sent as a negotiator to save the hostage.

import pygame
import pygame_menu

import Cutscenes
import RK800


def achievements():
    pass


def play_game():
    pass


# initializing the constructor
pygame.init()

# screen resolution
res = (1920, 1080)

# opens up a window
screen = pygame.display.set_mode(res)


menu = pygame_menu.Menu('The Hostage', 1920, 1080, theme=pygame_menu.themes.THEME_BLUE)


menu.add.button('Play', play_game)
menu.add.button('Achievements', achievements)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen)
