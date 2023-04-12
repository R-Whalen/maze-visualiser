import sys

# UTILITY FUNCTIONS

def canMove(current, neighbour):
    # only have to check for current walls as this is accounted for when mazes are being generated
    
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


# MAIN PATHFINDING FUNCTIONS

def astar(start, end, maze, board, weighted):
    start.distance = 0
    visited = set()
    
    entry = 0
    queue = PriorityQueue()
    