from globals import *
from display import *
import random

def recursiveBacktracking(start, end, board, quickMaze):
    # setup
    deadend = []
    
    # start explicitly at our start node
    current = start
    
    while len(deadend) != (cells * cells):
        current.visited = True
        
        # visit current
        current.colour = VISITED_COLOUR
        
        # assemble full list of all touching neighbours of our current node
        unvisited = [neighbour for neighbour in current.neights if neighbour.visited is False]
        
        # if our current has neighbours
        if len(unvisited):
            neighbour = random.choice(unvisited)
        else:
            # backtrack
            current.colour = PATH_COLOUR # signify backtracking with PATH_COLOUR
            current = current.parent
            deadend.append(current)
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
    nodes = [node for row in board for node in row]
    confirmed = {set: [node] for set, node in enumerate(nodes)}
    
    edges = []
    for row in range(cells):
        for col in range(cells):
            edges.append((board[row][col], board[row + 1][col], 'R')) if row < cells - 1 else None
            edges.append((board[row][col], board[row][col + 1], 'U')) if col < cells - 1 else None
            
    random.shuffle(edges)
    
    for (a, b, direction) in edges:
        if len(confirmed) == 1:
            break
        confirmedA, confirmedB = None, None
        for node in list(confirmed.keys()):
            if a in confirmed[node]:
                confirmedA = node
            if b in confirmed[node]:
                confirmedB = node
            if None not in (confirmedA, confirmedB) and confirmedA != confirmedB:
                confirmed[confirmedA].extend(confirmed[confirmedB])
                del confirmed[confirmedB]
                if direction == 'U':
                    a.walls[2] = False
                    b.walls[0] = False
                elif direction == 'R':
                    a.walls[3] == False
                    b.walls[1] == False
                    
                a.colour = VISITED_COLOUR
                b.colour = VISITED_COLOUR
                
                if quickMaze is False:
                    redrawWindow(start, end, board, False, True)
                break           
    
def eller(start, end, board, quickMaze):
    current = [n for n in range(0, len(board))]
    
    # loop over each row
    for row in board:
        for i, node in enumerate(row[:-1]):
            # if this is the last row or the adjacent cell doesn't belong to the same set, merge the 2 cells
            if (random.randint(0, 1) or row == board[-1]) and current[i] != current[i + 1]:
                if row != board[-1]:
                    current[i + 1] = current[i]
                # carve walls vertically
                node.walls[2] = False
                row[i + 1].walls[0] = False
                
                node.colour = VISITED_COLOUR
                row[i + 1].colour = VISITED_COLOUR
            
            # rerender
            if quickMaze is False:
                redrawWindow(start, end, board, False, True)
                
        # make vertical connections if we are not on the last row
        if row != board[-1]:
            switch = [n for n in range((board.index(row)+1) * len(row), (board.index(row)+2) * len(row))]
            moved = set()
            
            while set(current) != moved:
                for i, node in enumerate(row):
                    if random.randint(0, 1) and current[i] not in moved:
                        moved.add(current[i])
                        switch[i] = current[i]
                        # carve walls horizontally
                        node.walls[3] = False
                        board[board.index(row) + 1][i].walls[1] = False
                        
                        node.colour = PATH_COLOUR
                        board[board.index(row) + 1][i].colour = PATH_COLOUR
                        # rerender
                        if quickMaze is False: 
                            redrawWindow(start, end, board, False, True)
            
            # create vertical lines on the penultimate row so our last row will have a set with more than 1 cell so 
            # we can make a wall and not look empty
            if row == board[-2]:
                for i, node in enumerate(row):
                    if random.randint(0, 1) and node.walls[3] is True:
                        switch[i] = current[i]
                        # carve horizontally
                        node.walls[3] = False
                        board[board.index(row) + 1][i].walls[1] = False
                        
                        node.colour = PATH_COLOUR
                        board[board.index(row) + 1][i].colour = PATH_COLOUR
                        
                        if quickMaze is False:
                            redrawWindow(start, end, board, False, True)
            
        current = switch
            
                

def prim(start, end, board, quickMaze):
    maxBoardIndex = len(board) - 1 # relies on x * x dimensions
    current = board[random.randint(0, maxBoardIndex)][random.randint(0, maxBoardIndex)] # select random point to begin
    
    d = {frontier: current for frontier in current.neighbours}
    
    while d != {}:
        frontier, current = random.choice(list(d.items()))
        del d[frontier]
        frontier.visited = True
        
        for neighbour in frontier.neighbours:
            if neighbour.visited is False:
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