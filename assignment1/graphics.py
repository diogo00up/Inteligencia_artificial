import time
from gameLogic import *
from algorithms import *
import sys
import pygame
import math

from monteCarlo import monte_carlo_tree_search

BLACK = (0, 0, 0)
WHITE = (220, 220, 220)
GREY = (100, 100, 100)
LGREY = (180, 180, 180)
BLUE = (0, 0, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 400
GAME_HEIGHT = 400
GAME_WIDTH = 400

game = Game([], "x")
game.buildBoard()

def main():
    '''
    Initializes the pygame window and handles the choice of mode and algorithms
    '''
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)
    drawGrid(game)
    mode = None

    while True:
        drawMenu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if(event.type == pygame.MOUSEBUTTONDOWN):
                mode = menuMBdownHandler()

        pygame.display.update()
        if mode: break

    match mode:
        case 1:
            PvPloop()
        case 2:
            alg = 0
            while True:
                drawAlg()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        alg = AlgMBdownHandler()

                if alg != 0: break
            PvAIloop(alg)
        case 3:
            alg1 = 0
            alg2 = 0
            while True:
                drawAlg()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if alg1 == 0:
                            alg1 = AlgMBdownHandler()
                        else: alg2 = AlgMBdownHandler()

                if alg1 != 0 and alg2 != 0: break
            AIvAIloop(alg1, alg2)

def PvPloop():
    '''
    Player agaisnt Player game loop
    '''
    sel = None
    SCREEN.fill(WHITE, (0, 0, 400, 404))
    pygame.display.update()
    drawGrid(game)
    while True:

        if game.gameStatus == ERROR:
            sys.exit(0)
        if game.gameStatus == DRAW or game.gameStatus == PLAYERX or game.gameStatus == PLAYERO:
            if game.gameStatus == DRAW:
                drawInfo("Result: Draw")
                pygame.display.update()
            if game.gameStatus == PLAYERX:
                drawInfo("Result: Player X Won")
                pygame.display.update()
            if game.gameStatus == PLAYERO:
                drawInfo("Result: Player O Won")
                pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        sys.exit()

        if game.currPlayer == "x":
            drawInfo("Player X's turn")
        else:
            drawInfo("Player O's turn")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if(event.type == pygame.MOUSEBUTTONDOWN):
                SCREEN.fill(WHITE, (0, 0, 400, 404))
                sel = gameMBdownHandler(sel)
                drawGrid(game)
        
        pygame.display.update()

def PvAIloop(alg):
    '''
    Player against AI game loop

    Args:
        alg-> algorithm chosen for AI
    '''

    sel = None
    SCREEN.fill(WHITE, (0, 0, 400, 404))
    pygame.display.update()
    drawGrid(game)
    while True:
        if game.gameStatus == ERROR:
            sys.exit(0)
        if game.gameStatus == DRAW or game.gameStatus == PLAYERX or game.gameStatus == PLAYERO:
            if game.gameStatus == DRAW:
                drawInfo("Result: Draw")
                pygame.display.update()
            if game.gameStatus == PLAYERX:
                drawInfo("Result: Player X Won")
                pygame.display.update()
            if game.gameStatus == PLAYERO:
                drawInfo("Result: Player O Won")
                pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        sys.exit()

        if game.currPlayer == "x":
            drawInfo("Player X's turn")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if(event.type == pygame.MOUSEBUTTONDOWN):
                    SCREEN.fill(WHITE, (0, 0, 400, 404))
                    sel = gameMBdownHandler(sel)
                    drawGrid(game)
        else:
            drawInfo("AI's turn")
            if alg == 1:
                evaluation, move = minimax([0.9715506728775545, 0.2982760693711492, 0.5341823973706639, 0.8816659569127576, 0.45397536154791884, 0.6101822604987024, 0.043107966089507725], game, 2)
            else:
                move = monte_carlo_tree_search(game)

            game.move(move[0], move[1], move[2])

            SCREEN.fill(WHITE, (0, 0, 400, 404))
            drawGrid(game)

        pygame.display.update()

def AIvAIloop(alg1, alg2):
    '''
    AI against AI game loop

    Args:
        alg1-> algorithm chosen for AI X
        alg2-> algorithm chosen for AI O
    '''
    while True:
        if game.gameStatus == ERROR:
            sys.exit(0)
        if game.gameStatus == DRAW or game.gameStatus == PLAYERX or game.gameStatus == PLAYERO:
            if game.gameStatus == DRAW:
                drawInfo("Result: Draw")
                pygame.display.update()
            if game.gameStatus == PLAYERX:
                drawInfo("Result: Player X Won")
                pygame.display.update()
            if game.gameStatus == PLAYERO:
                drawInfo("Result: Player O Won")
                pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        sys.exit()

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        print("waiting for next turn", flush=True)
        drawInfo("Touch the screen for the next turn")
        while True:
            pygame.display.update()
            tmp = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tmp = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if tmp == True: break

        if game.currPlayer == "x":
            if alg1 == 1:
                evaluation, move = minimax([0.9715506728775545, 0.2982760693711492, 0.5341823973706639, 0.8816659569127576, 0.45397536154791884, 0.6101822604987024, 0.043107966089507725], game, 2)
            else:
                move = monte_carlo_tree_search(game)
            game.move(move[0], move[1], move[2])
            SCREEN.fill(WHITE, (0, 0, 400, 404))
            drawGrid(game)
        else:
            if alg2 == 1:
                evaluation, move = minimax([0.9715506728775545, 0.2982760693711492, 0.5341823973706639, 0.8816659569127576, 0.45397536154791884, 0.6101822604987024, 0.043107966089507725], game, 2)
            else:
                move = monte_carlo_tree_search(game)
            game.move(move[0], move[1], move[2])
            SCREEN.fill(WHITE, (0, 0, 400, 404))
            drawGrid(game)

        pygame.display.update()

def drawGrid(state):
    '''
    Draw grid and board pieces

    Args:
        state-> game state
    '''
    lines = len(state.board)
    columns = len(state.board[0])
    font = pygame.font.SysFont('Arial', 24)

    window_width = []
    window_height = []
    for x in range(0, GAME_WIDTH, math.ceil(GAME_WIDTH/columns)):
        window_width.append(x)
    for x in range(0, GAME_HEIGHT, math.ceil(GAME_HEIGHT/lines)):
        window_height.append(x)
        
    offset = (GAME_WIDTH/columns)/4
    for i, x in enumerate(window_width):
        for j, y in enumerate(window_height):
            rect = pygame.Rect(x, y, math.ceil(GAME_WIDTH/columns), math.ceil(GAME_HEIGHT/lines))
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            if(state.board[j][i] == "."):
                continue
            elif(state.board[j][i] == "x" or state.board[j][i] == "X"):
                color = RED
            else:
                color = BLUE

            if(state.board[j][i] == "X" or state.board[j][i] == "O"):
                font.bold = True
            else:
                font.bold = False
            img = font.render(state.board[j][i], True, color)
            SCREEN.blit(img, (x + offset + 4, y + offset - 2))

def drawMenu():
    '''
    Draw the mode menu

    '''
    SCREEN.fill(BLACK, (0, 404, 400, 500))
    font = pygame.font.SysFont('Arial', 24)

    for option in range(0, 3):
        if option == 0:
            text = font.render(" PvP ", True, WHITE, GREY)
        elif option == 1:
            text = font.render(" PvAI ", True, WHITE, GREY)
        else:
            text = font.render(" AIvAI ", True, WHITE, GREY)
        x = (option * 100) + (option + 1) * 25 + 50 
        text_rect = text.get_rect(center = (x, 450))
        SCREEN.blit(text, text_rect)

def menuMBdownHandler():
    '''
    Handles a mouse click in the mode menu

    '''
    pos = pygame.mouse.get_pos()
    if 425 <= pos[1] <= 470:
        if 45 <= pos[0] <= 105:
            print("PvP Selected", flush=True)
            return 1
        elif 170 <= pos[0] <= 230:
            print("PvAI Selected", flush=True)
            return 2
        elif 295 <= pos[0] <= 440:
            print("AIvAI Selected", flush=True)
            return 3

def drawAlg():
    '''
    Draw the algorithm menu

    '''
    SCREEN.fill(BLACK, (0, 404, 400, 500))
    font = pygame.font.SysFont('Arial', 24)

    for option in range(0, 2):
        if option == 0:
            text = font.render(" Minimax ", True, WHITE, GREY)
        elif option == 1:
            text = font.render(" Monte Carlo ", True, WHITE, GREY)
        x = (option * 175) + (option + 1) * 20 + 75 
        text_rect = text.get_rect(center = (x, 450))
        SCREEN.blit(text, text_rect)

def AlgMBdownHandler():
    '''
    Handles a mouse click in the algorithm menu

    '''
    pos = pygame.mouse.get_pos()
    if 425 <= pos[1] <= 470:
        if 45 <= pos[0] <= 145:
            print("Minimax Selected", flush=True)
            return 1
        elif 225 <= pos[0] <= 355:
            print("Monte Carlo Selected", flush=True)
            return 2

def drawInfo(info):
    '''
    Draw a string in the bottom panel of the window

    Args: 
        info-> string to write

    '''
    SCREEN.fill(BLACK, (0, 404, 400, 500))

    font = pygame.font.SysFont('Arial', 24)
    text = font.render(info, True, WHITE)
    text_rect = text.get_rect(center = (200, 450))
    SCREEN.blit(text, text_rect)
    
def gameMBdownHandler(sel):
    '''
    Handle a mouse click during the game

    Args: 
        sel-> selected board piece

    '''
    SCREEN.fill(WHITE, (0, 0, 400, 404))
    pos = pygame.mouse.get_pos()
    if not sel:
        SCREEN.fill(WHITE, (0, 0, 400, 404))
        if pos[0] <= 400 and pos[1] <= 400:
            sel = ( math.ceil(pos[0]/(GAME_WIDTH/len(game.board[0])))-1,  math.ceil(pos[1]/(GAME_WIDTH/len(game.board)))-1)
            if game.board[sel[1]][sel[0]] == ".": return None
            elif (game.board[sel[1]][sel[0]] == "o" or game.board[sel[1]][sel[0]] == "O") and game.currPlayer == "x": return None
            elif (game.board[sel[1]][sel[0]] == "x" or game.board[sel[1]][sel[0]] == "X") and game.currPlayer == "o": return None
            drawInfo(str(sel))
            cellSelection(sel)
            return sel
        else:
            drawInfo(str(pygame.mouse.get_pos()))
    else:
        SCREEN.fill(WHITE, (0, 0, 400, 404))
        direction = ""
        celldir = ( math.ceil(pos[0]/(GAME_WIDTH/len(game.board[0])))-1,  math.ceil(pos[1]/(GAME_WIDTH/len(game.board)))-1)
        if celldir == (sel[0]+1, sel[1]):
            direction = "right"
        elif celldir == (sel[0]-1, sel[1]):
            direction = "left"
        elif celldir == (sel[0], sel[1]+1):
            direction = "down"
        elif celldir == (sel[0], sel[1]-1):
            direction = "up"
        elif celldir == (sel[0]-1, sel[1]-1):
            direction = "upLeft"
        elif celldir == (sel[0]+1, sel[1]-1):
            direction = "upRight"
        elif celldir == (sel[0]-1, sel[1]+1):
            direction = "downLeft"
        elif celldir == (sel[0]+1, sel[1]+1):
            direction = "downRight"

        if direction != "":
            game.move(sel[1], sel[0], direction)
            SCREEN.fill(WHITE, (0, 0, 400, 404))
        
def cellSelection(cell):
    '''
    Draw a shadow on the selected board piece

    Args: 
        cell-> selected board piece

    '''
    SCREEN.fill(LGREY, (getcellTL(cell)[0], getcellTL(cell)[1],
                     math.ceil(GAME_WIDTH/len(game.board[0])), math.ceil(GAME_HEIGHT/len(game.board)) ))
    if cell[1] != 8:
        drawArrow((cell[0], cell[1]+1), "down")
        drawArrow((cell[0]+1, cell[1]+1), "downRight")
        drawArrow((cell[0]-1, cell[1]+1), "downLeft")
    drawArrow((cell[0], cell[1]-1), "up")
    drawArrow((cell[0]+1, cell[1]), "right")
    drawArrow((cell[0]-1, cell[1]), "left")
    drawArrow((cell[0]+1, cell[1]-1), "upRight")
    drawArrow((cell[0]-1, cell[1]-1), "upLeft")

def drawArrow(cell, direction):
    '''
    Draw a arrow in the adjacent tiles of the selected board piece

    Args: 
        cell-> selected board piece
        direction-> direction of the arrow

    '''
    x_offset = cell[0]*math.ceil(GAME_WIDTH/len(game.board[0]))
    y_offset = cell[1]*math.ceil((GAME_HEIGHT/len(game.board)))
    arrowSurface = pygame.Surface( (math.ceil(GAME_WIDTH/len(game.board[0])), math.ceil((GAME_HEIGHT/len(game.board)))) )
    arrowSurface.fill(WHITE)
    arrow = ((0, 18), (0, 28), (25, 28), (25, 38), (40, 23), (25, 8), (25, 18))
    diagArrow = ((0, 7), (0, 0), (7, 0), (25, 18), (32, 11), (35, 35), (11, 32), (18, 25))

    match direction:
        case "down":
            pygame.draw.polygon(arrowSurface, GREEN, arrow)
            arrowSurface = pygame.transform.rotate(arrowSurface, -90)
            SCREEN.blit(arrowSurface,(x_offset - 2, y_offset))
        case "up":
            pygame.draw.polygon(arrowSurface, GREEN, arrow)
            arrowSurface = pygame.transform.rotate(arrowSurface, 90)
            SCREEN.blit(arrowSurface,(x_offset - 3, y_offset + 4))
        case "left":
            pygame.draw.polygon(arrowSurface, GREEN, arrow)
            arrowSurface = pygame.transform.rotate(arrowSurface, 180)
            SCREEN.blit(arrowSurface,(x_offset, y_offset + 1))
        case "right":
            pygame.draw.polygon(arrowSurface, GREEN, arrow)
            SCREEN.blit(arrowSurface,(x_offset, y_offset))
        case "upRight":
            pygame.draw.polygon(arrowSurface, GREEN, diagArrow)
            arrowSurface = pygame.transform.rotate(arrowSurface, 90)
            SCREEN.blit(arrowSurface,(x_offset, y_offset + 4))
        case "upLeft":
            pygame.draw.polygon(arrowSurface, GREEN, diagArrow)
            arrowSurface = pygame.transform.rotate(arrowSurface, 180)
            SCREEN.blit(arrowSurface,(x_offset, y_offset))
        case "downLeft":
            pygame.draw.polygon(arrowSurface, GREEN, diagArrow)
            arrowSurface = pygame.transform.rotate(arrowSurface, -90)
            SCREEN.blit(arrowSurface,(x_offset - 5, y_offset))
        case "downRight":
            pygame.draw.polygon(arrowSurface, GREEN, diagArrow)
            SCREEN.blit(arrowSurface,(x_offset, y_offset))
    SCREEN.fill(BLACK, (0, 404, 400, 500))

def getcellTL(cell):
    '''
    Gets the x,y coordinates of the top left of a board piece

    Args: 
        cell-> selected board piece

    '''
    return cell[0]*(math.ceil(GAME_WIDTH/len(game.board[0]))), cell[1]*math.ceil((GAME_HEIGHT/len(game.board)))

main()