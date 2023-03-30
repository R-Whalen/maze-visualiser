from globals import *
import pygame
import sys

"""
    File to handle displaying and rendering information, only file present in the repository 
    that handles rendering
"""

# initialise our instance of pygame and define a set fps
pygame.init()
clock = pygame.time.Clock()
fps = 0

# pygame.surface is where everything is aligned properly, we use this to transform the current screen dimensions of the 
# user without not entirely breaking the responsiveness of the pygame application 
w = 1920
h = 1080
menu = pygame.Surface((w, h))
window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
width, height = window.get_width(), window.get_height()
cellWidth, cellHeight = width / cells, height / cells

ratio = (w / width + h / height) / 2
fontNum = pygame.font.SysFont(fontType, int(15 / ratio))

# basic function for rendering all node weights on the board
def updateWeights(start, end, board):
    for row in board:
        for node in row:
            if node.weight > 1 and node not in (start, end):
                number = fontNum.render(str(node.weight), True, BLACK)
                window.blit(number, (node.x * cellWidth + cellWidth // 2.5, node.y * cellHeight + 2))

# renders / fills in colour and walls for nodes
def updateTiles(start, end, board):
    def drawLine(pos1, pos2):
        pygame.draw.line(window, BLACK, (pos1, pos2))
    
    def fillBlock(block, colour):
        pygame.draw.rect(window, colour, block)
        
    for row in board:
        for node in row:
            # first we draw the walls of each node - calc position individually
            if node.walls[0] is True:
                drawLine((node.x * cellWidth, node.y * cellHeight), (node.x * cellWidth + cellWidth, node.y * cellHeight))
            if node.walls[1] is True:
                drawLine((node.x * cellWidth, node.y * cellHeight), (node.x * cellWidth, node.y * cellHeight + cellHeight))
            if node.walls[2] is True:
                drawLine((node.x * cellWidth, node.y * cellHeight + cellHeight), (node.x * cellWidth + cellWidth, node.y * cellHeight + cellHeight))
            if node.walls[3] is True:
                drawLine((node.x * cellWidth + cellWidth, node.y * cellHeight), (node.x * cellWidth + cellWidth, node.y * cellHeight + cellHeight))            
            # then we give our nodes their appropriate colours
            block = (node.x * cellWidth + 1, node.y * cellHeight + 1, cellWidth, cellHeight)
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
    
    window.fill(WHITE)
    updateTiles(start, end, board) # draw / handle nodes
    
    # node weight rendering routing
    if wg is True:
        updateWeights(start, end, board)
    
    # taking user input
    if running is True:
        for event in pygame.event.get():
            # fps controller - doubles and halves based on button press from mouse 4 and mouse 5 (side mouse buttons)
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 4:
                    fps *= 2 # double fps
                    # capping fps at 1000 so I dont blow my computer up
                    if fps >= 1000:
                        fps = 1000
                elif event.button == 5:
                    fps /= 2 # half fps
                    if fps < 1:
                        fps = 1 # fps cannot go below 1
            # basic exit handling
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    sys.exit()
                        
        clock.tick(fps) # +1 pygame tick
        
    pygame.display.update()