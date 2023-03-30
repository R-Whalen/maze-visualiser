import pygame.font
import os.path

"""
    This global file houses configurable variables that are going to be used across
    the main application (originating from main.py) 
"""

cells = 50 # changes visible cell count - higher number == increase the number of tiles on screen 

# preset colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
START_COLOUR = (255, 51, 0)
END_COLOUR = (51, 204, 51)
HOVERED = (0, 102, 0)
PATH_COLOUR = (255, 165, 0)
EXPAND_COLOUR = (130, 232, 130)
VISITED_COLOUR = (179, 249, 255)

# setup fonts
pygame.font.init()
lg_font = pygame.font.SysFont('arial', 75)
md_font = pygame.font.SysFont('arial', 50)
sm_font = pygame.font.SysFont('arial', 25)