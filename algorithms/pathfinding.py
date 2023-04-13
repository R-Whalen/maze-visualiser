from queue import PriorityQueue
from globals import *
from display import *
import time
import random

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

def findBiPath(pos1, pos2):
    path = findPath(pos2)[::-1]
    path.extend(findPath(pos1))
    
    return path

def buildPath(path, start, end, weighted, board):
    for node in path[::-1]:
        node.colour = PATH_COLOUR
        redrawWindow(start, end, board, weighted)

# MAIN PATHFINDING FUNCTIONS

def aStar(start, end, maze, board, weighted):
    # manually assign distance from start to start
    start.distanceFromStart = 0
    visited = set()

    entry = 0 # tracks entries in priority queue
    queue = PriorityQueue()
    
     #maintains we will always begin at the start node
    queue.put((manhattan(start, end), entry, start)) # queue item structure - score, entry, node
    
    while True:
        current = queue.get()[2]
        
        # formally "visit" current
        current.colour = VISITED_COLOUR
        visited.add(current)
        
        # exit loop - final act to build the path
        if current == end:
            path = findPath(end)
            buildPath(path, start, end, weighted, board)
            return
        
        for neighbour in current.neighbours:
            # exclude neighbours we cannot move to
            if canMove(current, neighbour) is False:
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

def bfs(start, end, maze, board, weighted):
    # setup
    queue = []
    visited = []
    
    queue.append(start)
    visited.append(start)

    while len(queue):
        current = queue.pop()
        current.colour = VISITED_COLOUR
        if current == end:
            path = findPath(end)
            buildPath(path, start, end, weighted, board)
            return
        
        for neighbour in current.neighbours:
            if canMove(current, neighbour) is False:
                continue
            
            if neighbour not in visited:
                neighbour.parent = current
                visited.append(neighbour)
                queue.append(neighbour)
                
        redrawWindow(start, end, board, weighted)
        
def bidirectionalDijkstra(start, end, maze, board, weighted):
    # setup
    start.distanceFromStart = 0
    end.distanceFromStart = 0 # treat both as start nodes
    
    visited = set()
    queue = PriorityQueue()
    entry = 0 # tracks entries in priority queue
    
    queue.put((0, entry, start, 'a'))
    entry += 1
    queue.put((0, entry, end, 'b'))
    
    while not queue.empty():
        # grab current node + if it came from start or end path
        *_, current, came = queue.get()
        # formally visit
        visited.add(current)
        current.colour = VISITED_COLOUR
        current.cameFrom = came
        
        for neighbour in current.neighbours:
            if canMove(current, neighbour) is False:
                continue
            
            # if we connect, intersection is found - complete path
            if current.cameFrom != neighbour.cameFrom and None not in (current.cameFrom, neighbour.cameFrom):
                if current.cameFrom == 'a':
                    a, b = current, neighbour
                else:
                    a, b = neighbour, current
                
                path = findBiPath(a, b)
                buildPath(path, start, end, weighted, board)
                return
        
            # dijkstra assign values based on weight + distance from start        
            temp = current.distanceFromStart + current.weight
            if temp < neighbour.distanceFromStart:
                neighbour.parent = current
                neighbour.distanceFromStart = temp
                entry += 1
                queue.put((temp, entry, neighbour, came))
                
        redrawWindow(start, end, board, weighted)
        
def dfs(start, end, maze, board, weighted):
    visited = set()
    queue = []
    
    queue.put(start)
    
    while len(queue):
        current = queue.pop(0)
        
        # completion 
        if current == end:
            path = findPath(end)
            buildPath(path, start, end, weighted, board)
            return
        
        if current not in visited:
            visited.add(current)
            
            for neighbour in current.neighbours:
                print('this')
                
def dijkstra(start, end, maze, board, weighted):
    # manually assign distance from start to start
    start.distanceFromStart = 0
    visited = set()

    entry = 0 # tracks entries in priority queue
    queue = PriorityQueue()
    
     #maintains we will always begin at the start node
    queue.put((manhattan(start, end), entry, start)) # queue item structure - score, entry, node
    
    while True:
        current = queue.get()[2]
        
        # formally "visit" current
        current.colour = VISITED_COLOUR
        visited.add(current)
        
        # exit loop - final act to build the path
        if current == end:
            path = findPath(end)
            buildPath(path, start, end, weighted, board)
            return
        
        for neighbour in current.neighbours:
            # exclude neighbours we cannot move to
            if canMove(current, neighbour) is False:
                continue    
            
            temp = current.distanceFromStart + current.weight # weight initialised to 1
            if temp < neighbour.distanceFromStart and neighbour not in visited:
                neighbour.parent = current # keep parent parity
                neighbour.distanceFromStart = temp
                
                score = neighbour.distanceFromStart
                
                entry += 1
                queue.put((score, entry, neighbour))
        
        # rerender at the end of each iteration
        redrawWindow(start, end, board, weighted)
        
def randomWalk(start, end, maze, board, weighted):
    # randomise which neighbour we go to
    
    queue = []
    queue.append(start) #start at our beginning node
    
    # if there are no neighbours we haven't visited
    while len(queue):
        current = queue.pop(0)
        current.visited = True
        
        if current == end:
            path = findPath(end)
            buildPath(path, start, end, weighted, board)
            return
        
        current.colour = VISITED_COLOUR
        
        potential = []
        
        # assemble valid neighbours
        for neighbour in current.neighbours:
            # exclude neighbours we can't move to
            if canMove(current, neighbour) is False:
                continue
            # want to isolate unvisited neighbours
            if neighbour.visited is False:
                potential.append(neighbour)
                
        # if we have a valid neighbour to move to, we randomise between the set and move to it
        if len(potential) > 0:
            i = random.randint(0, len(potential) - 1) # randomly generate index
            selected = current.neighbours[current.neighbours.index(potential[i])]
            selected.parent = current # join 
            queue.append(selected) # add 
        # else backstep to the parent of the node and loop around again - backtracking is a small improvement on random walk 
        else:
            queue.append(current.parent)
            
        # rerender at the end of every loop
        redrawWindow(start, end, board, weighted)