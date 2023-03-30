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

def updateTiles(start, end, board):
    def drawLine(pos1, pos2):
        pygame.draw.line(WIN, BLACK, (pos1, pos2))
    
    def fillBlock(block, colour):
        pygame.draw.rect(WIN, colour, block)
        
    for row in board:
        for node in row:
            # first we draw the walls of each node - calc position individually
            if node.walls[0] is True:
                drawLine((node.x * currentWidth, node.y * currentHeight), (node.x * currentWidth + currentWidth, node.y * currentHeight))
            if node.walls[1] is True:
                drawLine((node.x * currentWidth, node.y * currentHeight), (node.x * currentWidth, node.y * currentHeight + currentHeight))
            if node.walls[2] is True:
                drawLine((node.x * currentWidth, node.y * currentHeight + currentHeight), (node.x * currentWidth + currentWidth, node.y * currentHeight + currentHeight))
            if node.walls[3] is True:
                drawLine((node.x * currentWidth + currentWidth, node.y * currentHeight), (node.x * currentWidth + currentWidth, node.y * currentHeight + currentHeight))            
            # then we give our nodes their appropriate colouring
            block = (node.x * currentWidth + 1, node.y * currentHeight + 1, currentWidth, currentHeight)
            if node.colour is not None:
                fillBlock(node.colour, block)
            if node.obstacle is True:
                fillBlock(BLACK, block)
            if node is start:
                fillBlock(START_COLOUR, block)
            if node is end:
                fillBlock(END_COLOUR, block)

# acts as our display function to refresh the screen state manually after all calculations have been made
def redrawWindow(start, end, board, wg=False, running=True):
    global fps
    
    WIN.fill(WHITE)
    updateTiles(start, end, board) # draw / handle nodes
    
    # taking user input
    if running is True:
        for event in pygame.event.get():
            # fps controller
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 4:
                    fps *= 2
                    # capping fps at 500 so I dont blow my computer up
                    if fps >= 500:
                        fps = 500
                elif event.button == 5:
                    fps /= 2
                    if fps < 1:
                        fps = 1
            # basic exit handling
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    sys.exit()
                        
        clock.tick(fps) # +1 pygame tick
        
    pygame.display.update()
        
    