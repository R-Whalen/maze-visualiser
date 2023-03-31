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
fontType = 'arial'
fontLG = pygame.font.SysFont(fontType, 75)
fontMD = pygame.font.SysFont(fontType, 50)
fontSM = pygame.font.SysFont(fontType, 25)
# --- STATIC TEXT GENERATION BELOW (COLOURS NOT PROGRAMMATIC) ---
# setup main menu text
menuHeader = fontLG.render('Pathfinding Algorithm Visualisation', True, BLACK)
menuAuthor = fontSM.render('by Robert Whalen', True, BLACK)
# setup maze generation option text
chooseMaze = fontMD.render('Maze generation algorithm(optional):', True, BLACK)
# setup pathfinding algorithm option text
choosePathfind = fontMD.render('Pathfinding algorithms:', True, BLACK)
