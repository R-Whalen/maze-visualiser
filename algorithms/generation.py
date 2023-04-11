from globals import *
from display import *
import random

def recursiveBacktracking(start, end, board, quickMaze):
    # setup
    visited = set()
    deadend = []
    
    # start explicitly at our start node
    current = start
    
    while len(deadend) != (cells * cells):
        visited.add(current)
        
        # visit current
        current.colour = VISITED_COLOUR
        
        # assemble full list of all touching neighbours of our current node
        unvisited = [neighbour for neighbour in current.neighbours if neighbour not in visited]
        
        # if our current has neighbours
        if len(unvisited):
            neighbour = random.choice(unvisited)
        else:
            # backtrack
            current.colour = PATH_COLOUR # signify backtracking with PATH_COLOUR
            current = current.parent
            if quickMaze is False: # only render if quickMaze is false - doesn't waste resources rendering
                redrawWindow(start, end, board, False, True)
            continue # loop back around after rerender
    
        # if neighbour carve out walls
        if current.x - neighbour.x == -1: # <-
            neighbour.walls[1] = False
            current.walls[3] = False
        elif current.x - neighbour.x == 1: # ->
            neighbour.walls[3] = False
            current.walls[1] = False
        elif current.y - neighbour.y == -1: # ^
            neighbour.walls[0] = False
            current.walls[2] = False
        elif current.y - neighbour.y == 1: # v
            neighbour.walls[2] = False
            current.walls[0] = False
            
        # manually assign parents to support backtracking
        neighbour.parent = current
        # shift current to our selected neighbour
        current = neighbour
        
        if quickMaze is False: # only render if quickMaze is false - doesn't waste resources rendering
                redrawWindow(start, end, board, False, True)
            
            

def kruskal(start, end, board, quickMaze):
    return True
    
def eller(start, end, board, quickMaze):
    return True

def prim(start, end, board, quickMaze):
    visited = set()
    maxBoardIndex = len(board) - 1 # relies on x * x dimensions
    current = board[random.randint(0, maxBoardIndex)][random.randint(0, maxBoardIndex)] # select random point to begin
    
    d = {frontier: current for frontier in current.neighbours}
    
    while d != {}:
        frontier, current = random.choice(list(d.items()))
        del d[frontier]
        visited.add(frontier)
        
        for neighbour in frontier.neighbours:
            if neighbour not in visited:
                d[neighbour] = frontier
                
        # carve walls from our current to our neighbours that have not been visited
        if current.x - frontier.x == -1: # <-
            frontier.walls[1] = False
            current.walls[3] = False
        elif current.x - frontier.x == 1: # ->
            frontier.walls[3] = False
            current.walls[1] = False
        elif current.y - frontier.y == -1: # ^
            frontier.walls[0] = False
            current.walls[2] = False
        elif current.y - frontier.y == 1: # v
            frontier.walls[2] = False
            current.walls[0] = False
            
        current.colour = VISITED_COLOUR
        frontier.colour = VISITED_COLOUR
        
        if quickMaze is False: 
            redrawWindow(start, end, board, False, True)
            
        current.colour = PATH_COLOUR
        frontier.colour = PATH_COLOUR