import testHelper
from algorithms.pathfinding import *
from algorithms.generation import *
from mainMenu import mainMenu
from display import *
from node import *
import time
import json

"""
    File that handles the execution of both types of algorithms. Also handles user input for 
    everything after the main menu.
"""

def execute(alg, maze, quickMaze, quickPathfind, weighted):
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

    def generateMaze():
        # track timing of the generation
        startTime = time.time()
        
        if maze == 'eller':
            eller(start, end, board, quickMaze)
        elif maze == 'kruskal':
            kruskal(start, end, board, quickMaze)
        elif maze == 'prim':
            prim(start, end, board, quickMaze)
        elif maze == 'backtracking':
            recursiveBacktracking(start, end, board, quickMaze)
            
        finishTime = time.time()
        
        if not alg: return # early exit to avoid reporting if an algorithm isnt chosen, maze generation exclusive
        
        # export = []
        
        # Code for exporting walls when no maze gen is selected
        # for row in board:
        #     exportRow = []
        #     for node in row:
        #         exportRow.append(node.walls)
        #     export.append(exportRow)
        #     with open('./export-maze.json', "w") as f:
        #         json.dump(export, f, indent=4, sort_keys=True)  
                
                
        return {
            'type': 'Maze Generation',
            'algorithm': maze,
            'size': str(cells) + ' x ' + str(cells),
            'time' : (finishTime - startTime) * 1000, # recorded as ms
            'arraySize': None, # none as maze generation entry
            'pathWeight': None, # none as maze generation entry
            'quickMaze': quickMaze,
            'quickPathfind': None # none as maze generation entry
        }
    
    def solveMaze():
        startTime = time.time()
        
        if alg == 'a*':
            [path, balloonSize] = aStar(start, end, board, quickPathfind, weighted)
        elif alg == 'bfs':
            [path, balloonSize] = bfs(start, end, board, quickPathfind, weighted)
        elif alg == 'bidirectional dijkstra':
            [path, balloonSize] = bidirectionalDijkstra(start, end, board, quickPathfind, weighted)
        elif alg == 'dfs':
            [path, balloonSize] = dfs(start, end, board, quickPathfind, weighted)
        elif alg == 'dijkstra':
            [path, balloonSize] = dijkstra(start, end, board, quickPathfind, weighted)
        elif alg == 'random':
            [path, balloonSize] = randomWalk(start, end, board, quickPathfind, weighted)
        else: 
            raise Exception('Unsupported pathfinding algorithm argument given.')
        
        finishTime = time.time()
        
        # build once a path has been found - render outside of timed function
        buildPath(path, start, end, weighted, board)
        
        # assemble total weight
        totalWeight = 0
        for x in path:
            totalWeight += x.weight 
        
        return {
            'type': 'Pathfinding',
            'algorithm': alg,
            'size': str(cells) + ' x ' + str(cells),
            'time' : (finishTime - startTime) * 1000, # recorded as ms
            'arraySize': balloonSize,
            'pathWeight': totalWeight,
            'quickMaze': None, # none as pathfinding entry
            'quickPathfind': quickPathfind
        }
        
    board = setup()
    
    # default start and end nodes - start top left, end bottom right
    start = board[0][0]
    end = board[cells - 1][cells - 1]
    
    # generate maze
    if maze is not None:
        results = generateMaze()
        testHelper.appendResult(results) # documenting the maze generation run
        resetNodes(board) # resets colours etc, reatains wall makeup
    else:
        # set the walls of all nodes to False
        for row in board:
            for node in row:
                node.walls[0] = False
                node.walls[1] = False
                node.walls[2] = False
                node.walls[3] = False
                
        # Code for importing walls when no maze gen is selected - cells must be the same as when generated
        # f = open('./export-maze.json')
        # data = json.load(f)
        # f.close()
        
        # for i in range(len(board)):
        #     for j in range(len(board)):
        #         board[i][j].walls = data[i][j]
    
    if weighted is True:
        setRandomWeights(board)
        
    # user input + event handling
    begin, solved, draw, erase, pickStart, pickEnd, addWeight, selectCell, selectedCell = False, False, False, False, False, False, False, False, None
    
    # main loop
    while True:
        redrawWindow(start, end, board, weighted, True)
        
        # execute solve
        if begin is True:
            results = solveMaze()
            testHelper.appendResult(results) # documenting the pathfinding run 
            solved = True
            draw, begin = False, False
            
        # user input - event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            # set draw or erase to True or False if left or right click is being held 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if selectCell is True:
                        selectCell = True
                    else:
                        draw = True
                elif event.button == 3:
                    erase = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if selectCell is True:
                        selectCell = False
                    draw = False
                elif event.button == 3: 
                    erase = False
                     
            elif event.type == pygame.KEYDOWN:
                # user adding weights - only check if enabled
                if addWeight is True:
                    # selectedNumber map lets us narrow down user keyboard input later 
                    selectedNumber = {
                        pygame.K_1: 1,
                        pygame.K_2: 2,
                        pygame.K_3: 3,
                        pygame.K_4: 4,
                        pygame.K_5: 5,
                        pygame.K_6: 6,
                        pygame.K_7: 7,
                        pygame.K_8: 8,
                        pygame.K_9: 9
                    }
                    pressed = selectedNumber.get(event.key, None) # map event to number
                    if pressed is not None:
                        selectedCell.weight = pressed # assign weight to node
                        selectedCell.colour = None
                        addWeight = False
                # basic user input
                if event.key == pygame.K_RETURN:
                    begin = True
                # close application on 'q' or escaped
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_m:        
                    mainMenu()
                elif event.key == pygame.K_r:
                    solved = False
                    resetNodes(board)
                elif event.key == pygame.K_w:
                    selectCell = True 
                elif event.key == pygame.K_s:
                    pickStart = True
                elif event.key == pygame.K_e:
                    pickEnd = True
            # disabling on key up
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    pickStart = False
                elif event.key == pygame.K_e:
                    pickEnd = False
                elif event.key == pygame.K_w:
                    selectCell = False
                    addWeight = True
                    
        # handles all user altering maze prior to solving
        if solved is False:
            # placing start
            if pickStart is True or pickEnd is True:
                #sanitising coords
                x, y = getMouseCoords()
                if x and y and pickStart and board[x][y] != end:
                    start = board[x][y]
                if pickEnd and board[x][y] != start: 
                    end = board[x][y]
                        
            if maze is None:
                if selectCell is True:
                    x, y = getMouseCoords()
                    if selectedCell is not None:
                        selectedCell.colour = WHITE
                    if x and y:
                        selectedCell = board[x][y]
                        selectedCell.colour = VISITED_COLOUR
                
                # drawing logic
                if draw is True:
                    x, y = getMouseCoords()
                    if x and y:
                        board[x][y].obstacle = True
                if erase is True:
                    x, y = getMouseCoords()
                    if x and y:
                        board[x][y].obstacle = False
