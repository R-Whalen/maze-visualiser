import run
from display import *
from globals import *

#util function for blitting
def blit(vis, pos):
    return menu.blit(vis, pos)

def genText(hover, maze, pathfind, eMaze, ePathfind, quickMaze = False, weighted = False):
    # menu header + author
    blit(menuHeader, (170,50))
    blit(menuAuthor, (1000, 140))
    
    mazeColours = [BLACK] * 3
    colours = [BLACK] * 1
    # set selected to black
    if ePathfind is not None:
        colours[ePathfind] = BLACK
    if eMaze is not None: 
        colours[eMaze] = BLACK
        
    if hover is not None:
        if hover <= 2:
            colours[hover] = HOVERED
        elif hover != 7:
            mazeColours[hover - 1] = HOVERED
        else:
            mazeColours[4] = HOVERED
            
    if pathfind is not None:
        colours[pathfind] = END_COLOUR
    if maze is not None:
        mazeColours[maze] = END_COLOUR
    if quickMaze is not False:
        mazeColours[1] = END_COLOUR
    if weighted is not False:
        mazeColours[2] = END_COLOUR
    
    if quickMaze is False:
        quickMazeText = fontSM.render('Instant Maze Generation?', True, mazeColours[1])
    else:
        quickMazeText = fontSM.render('Instant Maze Generation!', True, mazeColours[1])
        
    if weighted is False:
        weightedText = fontSM.render('Randomise cell weights?', True, mazeColours[2])
    else:
        weightedText = fontSM.render('Randomise cell weights!', True, mazeColours[2])
        
    renderQuickMaze = blit(quickMazeText, (90, 800))
    renderWeighted = blit(weightedText, (90, 845))
        
    # pathfinding options text
    blit(choosePathfind, (85, 400))
    pfPrim = fontSM.render('* PRIM\'S ALGORITHM', True, mazeColours[0])
    renderPfPrim = blit(pfPrim, (630, 725))
    
    # maze generation text
    blit(chooseMaze, (85,600))
    mgAStar = fontSM.render('* A* ALGORITHM', True, colours[0])
    renderMgPrim = blit(mgAStar, (630,390))
    
    return renderPfPrim, renderMgPrim

def mainMenu():
    pathfindAlgs = ['a*']
    mazeGenAlgs = ['recursive', 'kruskal', 'eller', 'prim']
    hover, maze, pathfind, eMaze, ePathfind, quickMaze, weighted = None, None, None, None, None, False, False
    
    while True:
        # fill white background + generate menu text
        menu.fill(WHITE)
        rects = genText(hover, maze, pathfind, eMaze, ePathfind, quickMaze, weighted)
        
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
                        if chosen <= len(pathfindAlg) - 1:
                            pathfind = chosen
                            ePathfind = None
                        elif chosen < (len(pathfindAlg) + len(mazeGenAlgs)) - 2:
                            maze = chosen-1
                            eMaze = None
                            weighted = False
                        elif chosen == (len(pathfindAlg) + len(mazeGenAlgs)) - 1:
                            if maze is not None:
                                quickMaze = True
                        elif chosen == len(pathfindAlg) + len(mazeGenAlgs):
                            if maze is None:
                                weighted = True
                elif event.button == 3:
                    click = [rect.collidepoint((x, y)) for rect in rects]
                    if 1 in click:
                        undone = click.index(1)
                        if undone <= 2:
                            ePathfind = undone
                            if pathfind == ePathfind:
                                pathfind = None
                        elif undone < 7:
                            eMaze = undone-1
                            if maze == eMaze:
                                maze = None
                                quickMaze = False
                        elif undone == 7:
                            quickMaze = False
                        elif undone == 8:
                            weighted = False
        
        hover = [rect.collidepoint((x, y)) for rect in rects]
        if 1 in hover:
            hover = hover.index(1)
        else:
            hover = None
            
        # adapt menu to screen dimensions + update
        window.blit(pygame.transform.scale(menu, window.get_rect().size), (0, 0))
        pygame.display.update()
            
        