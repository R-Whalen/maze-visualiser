import run
from display import *
from globals import *

#util function for blitting
def blit(vis, pos):
    return menu.blit(vis, pos)

def genText(pathfindAlgs, mazeGenAlgs, hover, maze, pathfind, eMaze, ePathfind, quickMaze = False, weighted = False):
    # menu header + author
    blit(menuHeader, (170,50))
    blit(menuAuthor, (1000, 140))
    
    # calc pathfinding + maze generation colour array lengths
    pathfindAlgsLength, mazeGenAlgsLength = 0, 0
    if (len(pathfindAlgs)):
        pathfindAlgsLength = len(pathfindAlgs) - 1
    if (len(mazeGenAlgs)):
        mazeGenAlgsLength = len(mazeGenAlgs) - 1
    
    pathfindingColours = [BLACK] * len(pathfindAlgs)
    mazeColours = [BLACK] * (len(mazeGenAlgs) + 2) # add 2 indices for quickMaze and weighting
    # set selected to black
    if ePathfind is not None:
        pathfindingColours[ePathfind] = BLACK
    if eMaze is not None: 
        mazeColours[eMaze] = BLACK

    # hover colour transition handling
    if hover is not None:
        if hover < len(pathfindAlgs):
            pathfindingColours[hover] = HOVERED
        else:
            mazeColours[hover - len(pathfindAlgs)] = HOVERED
            
    if pathfind is not None:
        pathfindingColours[pathfind] = END_COLOUR
    if maze is not None:
        mazeColours[maze] = END_COLOUR
    if quickMaze is not False:
        mazeColours[len(mazeGenAlgs)] = END_COLOUR
    if weighted is not False:
        mazeColours[len(mazeGenAlgs) + 1] = END_COLOUR
    
    # pathfinding text
    blit(choosePathfind, (85, 500)) # heading
    pfAStar = fontSM.render('* A* ALGORITHM', True, pathfindingColours[0])
    renderPfA = blit(pfAStar, (85, 575))
    
    # maze generation options text
    blit(chooseMaze, (85, 750)) # heading
    mgEller = fontSM.render('* ELLER\'S ALGORITHM', True, mazeColours[0])
    renderMgEller = blit(mgEller, (85, 825))
    mgKruskal = fontSM.render('* KRUSKAL\'S ALGORITHM', True, mazeColours[1])
    renderMgKruskal = blit(mgKruskal, (400, 825))
    mgPrim = fontSM.render('* PRIM\'S ALGORITHM', True, mazeColours[2])
    renderMgPrim = blit(mgPrim, (85, 875))
    mgBacktracking = fontSM.render('* RECURSIVE BACKTRACKING', True, mazeColours[3])
    renderMgBacktracking = blit(mgBacktracking, (400, 875))
    
    # variable blitted text 
    if quickMaze is False:
        quickMazeText = fontSM.render('Instant Maze Generation?', True, mazeColours[len(mazeGenAlgs)])
    else:
        quickMazeText = fontSM.render('Instant Maze Generation!', True, mazeColours[len(mazeGenAlgs)])
        
    if weighted is False:
        weightedText = fontSM.render('Randomise cell weights?', True, mazeColours[len(mazeGenAlgs) + 1])
    else:
        weightedText = fontSM.render('Randomise cell weights!', True, mazeColours[len(mazeGenAlgs) + 1])
        
    renderQuickMaze = blit(quickMazeText, (700, 1000))
    renderWeighted = blit(weightedText, (1020, 1000))
    
    # package returned values
    returned = [
        # pathfind
        renderPfA,
        # maze gen
        renderMgEller,
        renderMgKruskal,
        renderMgPrim,
        renderMgBacktracking,
        # options
        renderQuickMaze,
        renderWeighted
    ]
    
    return returned

def mainMenu():
    pathfindAlgs = ['a*']
    mazeGenAlgs = ['eller', 'kruskal', 'prim', 'backtracking']
    hover, maze, pathfind, eMaze, ePathfind, quickMaze, weighted = None, None, None, None, None, False, False
    
    while True:
        # fill white background + generate menu text
        menu.fill(WHITE)
        rects = genText(pathfindAlgs, mazeGenAlgs, hover, maze, pathfind, eMaze, ePathfind, quickMaze, weighted)
        
        # event handling
        x, y = pygame.mouse.get_pos()
        x, y = x / (window.get_width() / menu.get_width()), y / (window.get_height() / menu.get_height())
        
        for event in pygame.event.get():
            # handling meta events
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    pathfindAlg = pathfindAlgs[pathfind] if pathfind is not None else None
                    mazeGenAlg = mazeGenAlgs[maze] if maze is not None else None
                    if pathfindAlg is not None:
                        run.execute(pathfindAlg, mazeGenAlg, quickMaze, weighted)
            # rect selection - manual wiring
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = [rect.collidepoint((x, y)) for rect in rects]
                    if 1 in click:
                        chosen = click.index(1)
                        if chosen < len(pathfindAlgs):
                            pathfind = chosen
                            ePathfind = None
                        elif chosen < (len(pathfindAlgs) + len(mazeGenAlgs)):
                            maze = chosen - 1
                            eMaze = None
                            weighted = False
                        elif chosen == (len(pathfindAlgs) + len(mazeGenAlgs)):
                            if maze is not None:
                                quickMaze = True
                        elif chosen == len(pathfindAlgs) + len(mazeGenAlgs) + 1:
                            if maze is None:
                                weighted = True
                elif event.button == 3:
                    click = [rect.collidepoint((x, y)) for rect in rects]
                    if 1 in click:
                        undone = click.index(1)
                        if undone < len(pathfindAlgs):
                            ePathfind = undone
                            if pathfind == ePathfind:
                                pathfind = None
                        elif undone < (len(pathfindAlgs) + len(mazeGenAlgs)):
                            eMaze = undone - 1
                            if maze == eMaze:
                                maze = None
                                quickMaze = False
                        elif undone == (len(pathfindAlgs) + len(mazeGenAlgs)):
                            quickMaze = False
                        elif undone == (len(pathfindAlgs) + len(mazeGenAlgs) + 1):
                            weighted = False
        
        hover = [rect.collidepoint((x, y)) for rect in rects]
        if 1 in hover:
            hover = hover.index(1)
        else:
            hover = None
            
        # adapt menu to screen dimensions + update
        window.blit(pygame.transform.scale(menu, window.get_rect().size), (0, 0))
        pygame.display.update()