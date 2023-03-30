from globals import cells

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]
        self.neighbours = []
        self.distanceFromStart = float('inf') # float('inf') acts as an absolute upper bound
        self.distanceToEnd= float('inf')
        self.color = None
        self.obstacle = None
        self.expanding = None
        self.parent = None