from algorithms.pathfinding import *
from algorithms.generation import *
from run import *
from mainMenu import *
from display import *
from globals import *
from node import *

if __name__ == "__main__":
    if cells < 2: raise Exception('Dimensions selected not supported (minimum of 2 is accepted)')
    pathfindAlg, mazeGenAlg, mazeGen, weight = mainMenu()
