from algorithms.pathfinding import *
from algorithms.generation import *
from menu import mainMenu
from display import *
from node import *

def setup():
    # declare board
    board = [[Node(x, y) for y in range(cells)] for x in range(cells)]
    
    # setting node neighbours (only traversal up-right-down-left are accepted movements)
    for row in board:
        for node in row:
            # checks up
            if node.y + 1 < cells:
                node.neighbours.append(board[node.x][node.y + 1])
            # checks right
            if node.x + 1 < cells:
                node.neighbours.append(board[node.x + 1][node.y])
            # checks down
            if node.y - 1 >= 0:
                node.neighbours.append(board[node.x][node.y - 1])
            # checks left
            if node.x - 1 >= 0:
                node.neighbours.append(board[node.x - 1][node.y])
    
    return board