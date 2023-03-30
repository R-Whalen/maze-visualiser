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
START_COLOR = (255, 51, 0)
END_COLOR = (51, 204, 51)
HOVERED = (0, 102, 0)
PATH_COLOR = (255, 165, 0)
EXPAND_COLOR = (130, 232, 130)
VISITED_COLOR = (179, 249, 255)