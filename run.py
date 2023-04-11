from algorithms.pathfinding import *
from algorithms.generation import *
from mainMenu import mainMenu
from display import *
from node import *

def execute(alg, maze, quickMaze, weighted):
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
        if maze == 'eller':
            
        elif maze == 'kruskal':

        elif maze == 'prim':

        elif maze == 'backtracking':
            
        # only possibility for no maze being selected is if we are using weights
        elif not weighted:
            raise Exception('Unsupported maze generation technique argument given.')
    
    def solveMaze():
        if alg == 'a*':
        else: 
            raise Exception('Unsupported pathfinding algorithm argument given.')
        
    board = setup()
    
    # default start and end nodes
    start = board[0][0]
    end = board[cells - 1][cells - 1]
    
    # generate maze
    if maze is not None:
        generateMaze(maze, board, quickMaze, start, end)
        resetNodes(board)
    
    if weighted is True:
        setRandomWeights(board)
        
    # user input + event handling
    begin, solved, draw, erase, pickStart, pickEnd, addWeight, selectCell, selectedCell = False, False, False, False, False, False, False, False, None
    
    # main loop
    while True:
        redrawWindow(start, end, board, weighted = False, running = True)
        
        # execute solve
        if begin is True:
            solveMaze(alg, board, quickMaze, start, end)
            solved = True
            
        # handles all user altering maze prior to solving
        if solved is False:
            # placing start
            if pickStart is True or pickEnd is True:
                #sanitising coords
                x, y = getMouseCoords()
                if pickStart and board[x][y] != end:
                    start = board[x][y]
                if pickEnd and board[x][y] != start: 
                    end = board[x][y]
                        
            if maze is None:
                if selectCell is True:
                    x, y = getMouseCoords()
                    if selectedCell is not None:
                        selectedCell.colour = WHITE
                    selectedCell = board[x][y]
                    selectedCell.colour = VISITED_COLOUR
                
                # drawing logic
                if draw is True:
                    x, y = getMouseCoords()
                    board[x][y].obstacle = True
                if erase is True:
                    x, y = getMouseCoords()
                    board[x][y].obstacle = False

        # user input - event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            # set draw or erase to True or False if left or right click is being held 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    selectCell = True
                    draw = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selectCell = False
                    draw = False
                if event.button == 3: 
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
                if event.key == pygame.pygame.K_RETURN:
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