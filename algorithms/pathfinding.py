from queue import PriorityQueue
from globals import *
from display import *

# UTILITY FUNCTIONS

def canMove(current, neighbour):
    # only have to check for current walls as this is accounted for when mazes are being generated
    # neighbour is an obstacle
    if neighbour.obstacle == True:
        return False
    # can move up
    if current.y - neighbour.y == 1 and current.walls[0] is True:
        return False
    # can move down
    if current.y - neighbour.y == -1 and current.walls[2] is True:
        return False
    # can move left
    if current.x - neighbour.x == 1 and current.walls[1] is True:
        return False
    # can move right
    if current.x - neighbour.x == -1 and current.walls[3] is True:
        return False
    
    # returns true if makes it past the if statement gauntlet
    return True

def manhattan(pos1, pos2):
    # returns manhattan distance between two nodes
    
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)

def findPath(pos):
    # find the path from a position to the start
    current = pos
    path = [current]
    
    while current.parent is not None:
        current = current.parent
        path.append(current)
        
    return path

def buildPath(path, start, end, weighted, board):
    for node in path[::-1]:
        node.colour = PATH_COLOUR
        redrawWindow(start, end, board, weighted)

# MAIN PATHFINDING FUNCTIONS

def astar(start, end, maze, board, weighted):
    # manually assign distance from start to start
    start.distanceFromStart = 0
    # assign manhattan distance
    visited = set()

    entry = 0
    queue = PriorityQueue()
    queue.put((manhattan(start, end), entry, start))
    
    while True:
        current = queue.get()[2]
        current.colour = VISITED_COLOUR
        
        # formally "visit" current
        visited.add(current)
        
        # exit loop - final act to build the path
        if current == end:
            path = findPath(end)
            buildPath(path, start, end, weighted, board)
            break
        
        for neighbour in current.neighbours:
            # exclude neighbours we cannot move to
            if maze is not None and canMove(current, neighbour) is False:
                continue    
            
            temp = current.distanceFromStart + current.weight # weight initialised to 1
            if temp < neighbour.distanceFromStart and neighbour not in visited:
                neighbour.parent = current # keep parent parity
                neighbour.distanceFromStart = temp
                
                # A* heuristic, utilises manhattan distance from position and adds it to the score
                neighbour.distanceToEnd = manhattan(neighbour, end)
                score = neighbour.distanceToEnd + neighbour.distanceFromStart
                
                entry += 1
                queue.put((score, entry, neighbour))
        
        # rerender at the end of each iteration
        redrawWindow(start, end, board, weighted)
        
    