from globals import cells
import random

"""
    Basic class definition for the basis of all of our working as far as pathfinding 
    and maze generation is concerned - the node
"""

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]
        self.neighbours = []
        self.weight = 1
        self.distanceFromStart = float('inf') # float('inf') acts as an absolute upper bound
        self.distanceToEnd= float('inf')
        self.colour = None
        self.obstacle = None
        self.parent = None
        self.visited = None
        self.cameFrom = None # implemented for simplifying bidirectional dijkstra
        
    # node.reset allows up to quickly reset the board before undergoing another set of generation
    def reset(self):
        self.distanceFromStart = float('inf')
        self.distanceToEnd = float('inf')
        self.colour = None
        self.parent = None
        self.obstacle = False
        self.visited = False
        self.cameFrom = None
        
    # helper function to locate random unvisited neighbour (will save a vast amount of time in the long run for maze generation algs)
    def getRandomNeighbour(self):
        pot = [neighbour for neighbour in self.neighbours if neighbour.visited is False]
        if not pot:
            return None
        else:
            return random.choice(pot)
        
# basic helper function for nodes
def resetNodes(board):
    for row in board:
        for node in row:
            node.reset()
        
# helper function to assign random weights to all available nodes
def setRandomWeights(board):
    # loops over every node and assigns a single digit weight 
    for node in random.sample([col for row in board for col in row], int(cells ** 2 * 0.33)):
        node.weight = random.randint(1,9)