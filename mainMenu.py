import run
from display import *
from globals import *

# util function for blitting
def blit(vis, pos):
    return menu.blit(vis, pos)

# util function for drawing rectangles
def rect(colour, options):
    return pygame.draw.rect(menu, colour, options, 4)

def fill(colour, rect):
    return menu.fill(colour, rect)

def genText(pathfindAlgs, mazeGenAlgs, hover, maze, pathfind, eMaze, ePathfind, quickMaze = False, quickPathfind = False, weighted = False):
    # menu header + author
    blit(menuHeader, (170,50))
    blit(menuAuthor, (1000, 140))
    
    # render legend
    rect(BLACK, (1400, 310, 300, 450))
    for i, text in enumerate(appLegend):
        imgPosition = (1450, 325 + i * 75, 50, 50)
        # handles variability in legend type, produces image
        if text == ' - start':
            fill(START_COLOUR, rect(START_COLOUR, imgPosition))
        elif text == ' - target':
            fill(END_COLOUR, rect(END_COLOUR, imgPosition))
        elif text == ' - visited':
            fill(VISITED_COLOUR, rect(VISITED_COLOUR, imgPosition))
        elif text == ' - path':
            fill(PATH_COLOUR, rect(PATH_COLOUR, imgPosition))
        elif text == ' - obstacle':
            fill(BLACK, rect(BLACK, imgPosition))
        elif text == ' - cell weight':
            fill(BLACK, rect(BLACK, imgPosition))
            fill(WHITE, rect(WHITE, (imgPosition[0] + 5, imgPosition[1] + 5, 40, 40)))
            blit(fontSM.render('7', True, BLACK), (imgPosition[0] + 20, imgPosition[1] + 10))
        blit(fontSM.render(text, True, BLACK), (1550, 335 + i * 75))        
    
    pathfindingColours = [BLACK] * len(pathfindAlgs)
    mazeColours = [BLACK] * (len(mazeGenAlgs) + 3) # add 3 indices for quickMaze, quickMaze and weighting
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
    if quickPathfind is True:
        mazeColours[len(mazeGenAlgs) + 1] = END_COLOUR
    if weighted is not False:
        mazeColours[len(mazeGenAlgs) + 2] = END_COLOUR
    
    # pathfinding text
    blit(choosePathfind, (85, 500)) # heading
    pfAStar = fontSM.render('* A* ALGORITHM', True, pathfindingColours[0])
    renderPfA = blit(pfAStar, (85, 575))
    pfBfs = fontSM.render('* BREADTH FIRST SEARCH', True, pathfindingColours[1])
    renderBfs = blit(pfBfs, (425, 575))
    pfBdD = fontSM.render('* BIDIRECTIONAL DIJKSTRA', True, pathfindingColours[2])
    renderBdD = blit(pfBdD, (85, 650))
    pfDfs = fontSM.render('* DEPTH FIRST SEARCH', True, pathfindingColours[3])
    renderDfs = blit(pfDfs, (425, 650))
    pfDijk = fontSM.render('* DIJKSTRA\'S ALGORITHM', True, pathfindingColours[4])
    renderDijk = blit(pfDijk, (85, 725))
    pfRW = fontSM.render('* RANDOM WALK', True, pathfindingColours[5])
    renderRW = blit(pfRW, (425, 725))
    
    # maze generation options text
    blit(chooseMaze, (85, 750)) # heading
    mgEller = fontSM.render('* ELLER\'S ALGORITHM', True, mazeColours[0])
    renderMgEller = blit(mgEller, (85, 825))
    mgKruskal = fontSM.render('* KRUSKAL\'S ALGORITHM', True, mazeColours[1])
    renderMgKruskal = blit(mgKruskal, (425, 825))
    mgPrim = fontSM.render('* PRIM\'S ALGORITHM', True, mazeColours[2])
    renderMgPrim = blit(mgPrim, (85, 875))
    mgBacktracking = fontSM.render('* RECURSIVE BACKTRACKING', True, mazeColours[3])
    renderMgBacktracking = blit(mgBacktracking, (425, 875))
    
    # variable blitted text 
    if quickMaze is False:
        quickMazeText = fontSM.render('Disable maze generation rendering?', True, mazeColours[len(mazeGenAlgs)])
    else:
        quickMazeText = fontSM.render('Disabled maze generation rendering!', True, mazeColours[len(mazeGenAlgs)])
        
    if quickPathfind is False:
        quickPathfindText = fontSM.render('Disable pathfinding rendering?', True, mazeColours[len(mazeGenAlgs) + 1])
    else:
        quickPathfindText = fontSM.render('Disabled pathfinding rendering!', True, mazeColours[len(mazeGenAlgs) + 1])
        
    
    if weighted is False:
        weightedText = fontSM.render('Randomise cell weights?', True, mazeColours[len(mazeGenAlgs) + 2])
    else:
        weightedText = fontSM.render('Randomise cell weights!', True, mazeColours[len(mazeGenAlgs) + 2])
        
        
    renderQuickMaze = blit(quickMazeText, (400, 1000))
    renderQuickPathfind = blit(quickPathfindText, (800, 1000))
    renderWeighted = blit(weightedText, (1200, 1000))
    
    # package returned values
    returned = [
        # pathfind
        renderPfA,
        renderBfs,
        renderBdD,
        renderDfs,
        renderDijk,
        renderRW,
        # maze gen
        renderMgEller,
        renderMgKruskal,
        renderMgPrim,
        renderMgBacktracking,
        # options
        renderQuickMaze,
        renderQuickPathfind,
        renderWeighted
    ]
    
    return returned

def mainMenu():
    pathfindAlgs = ['a*', 'bfs', 'bidirectional dijkstra', 'dfs', 'dijkstra', 'random']
    mazeGenAlgs = ['eller', 'kruskal', 'prim', 'backtracking']
    hover, maze, pathfind, eMaze, ePathfind, quickMaze, quickPathfind, weighted = None, None, None, None, None, False, False, False
    
    while True:
        # fill white background + generate menu text
        menu.fill(WHITE)
        rects = genText(pathfindAlgs, mazeGenAlgs, hover, maze, pathfind, eMaze, ePathfind, quickMaze, quickPathfind, weighted)
        
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
                        run.execute(pathfindAlg, mazeGenAlg, quickMaze, quickPathfind, weighted)
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
                            maze = chosen - len(pathfindAlgs)
                            eMaze = None
                            weighted = False
                        elif chosen == (len(pathfindAlgs) + len(mazeGenAlgs)):
                            if maze is not None:
                                quickMaze = True
                        elif chosen == len(pathfindAlgs) + len(mazeGenAlgs) + 1:
                            if pathfind is not None:
                                quickPathfind = True
                        elif chosen == len(pathfindAlgs) + len(mazeGenAlgs) + 2:
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
                            eMaze = undone - len(pathfindAlgs)
                            if maze == eMaze:
                                maze = None
                                quickMaze = False
                        elif undone == (len(pathfindAlgs) + len(mazeGenAlgs)):
                            quickMaze = False
                        elif undone == (len(pathfindAlgs) + len(mazeGenAlgs) + 1):
                            quickPathfind = False
                        elif undone == (len(pathfindAlgs) + len(mazeGenAlgs) + 2):
                            weighted = False
        
        hover = [rect.collidepoint((x, y)) for rect in rects]
        if 1 in hover:
            hover = hover.index(1)
        else:
            hover = None
            
        # adapt menu to screen dimensions + update
        window.blit(pygame.transform.scale(menu, window.get_rect().size), (0, 0))
        pygame.display.update()