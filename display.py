from globals import *
import pygame
import sys

"""
    File to handle displaying and rendering information, only file present in the repository 
    that handles rendering
"""

# initialise our instance of pygame and define a set fps (TODO: implement variable fps)
pygame.init()
clock = pygame.time.Clock()
fps = 0

# pygame.surface is where everything is aligned properly, we use this to transform the current screen dimensions of the 
# user without not entirely breaking the responsiveness of the pygame application 
menu = pygame.Surface((1920, 1080))
WIN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
width, height = WIN.get_width(), WIN.get_height()
currentWidth, currentHeight = width / cells, height / cells