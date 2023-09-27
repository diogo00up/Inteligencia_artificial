from gameLogic import *
from algorithms import *
from monteCarlo import *
import sys


def pvpLoop():
    '''
    Description:
        function responsible for a player vs play game 
    
    '''

    print("PLAYER VS PLAYER")

    gameState = Game([], "x")
    gameState.buildBoard()
    gameState.printGameState()

    while(True):
        line = int(input("Line? "))
        row = int(input("Row? "))
        direction = input("Direction? ")

        if(gameState.move(line, row, direction) == False):
            print("Invalid Move\n")
            continue
        if(gameState.gameStatus == ERROR):
            print("ERROR LINE 23\n")
            sys.exit(0)
        if(gameState.gameStatus == DRAW):
            print("\tResult: Draw\n")
            gameState.printGameState()
            break
        if(gameState.gameStatus == PLAYERX):
            print("\tResult: Player X Won\n")
            gameState.printGameState()
            break;
        if(gameState.gameStatus == PLAYERO):
            print("\tResult: Player O Won\n")
            gameState.printGameState()
            break;

        gameState.printGameState()

def pveLoop():
    '''
    Description:
        function responsible for a player vs AI using Minimax algorithm
    
    '''
    print("PLAYER VS AI")
    print("PLAYER = x")
    print("AI = o")

    gameState = Game([], "x")
    gameState.buildBoard()
    gameState.printGameState()

    while(True):

        if(gameState.currPlayer == "x"):

            line = int(input("Line? "))
            row = int(input("Row? "))
            direction = input("Direction? ")

            if(gameState.move(line, row, direction) == False):
                print("Invalid Move\n")
                continue
            if(gameState.gameStatus == ERROR):
                print("ERROR LINE 23\n")
                sys.exit(0)
            if(gameState.gameStatus == DRAW):
                print("\tResult: Draw\n")
                gameState.printGameState()
                break
            if(gameState.gameStatus == PLAYERX):
                print("\tResult: Player X Won\n")
                gameState.printGameState()
                break;
            if(gameState.gameStatus == PLAYERO):
                print("\tResult: Player O Won\n")
                gameState.printGameState()
                break;
        else:
            evaluation, bestMove = minimax([0.9715506728775545, 0.2982760693711492, 0.5341823973706639, 0.8816659569127576, 0.45397536154791884, 0.6101822604987024, 0.043107966089507725], gameState, 3)
            print("Best move = {}".format(bestMove))
            gameState.move(bestMove[0], bestMove[1], bestMove[2])

        gameState.printGameState()
        print(flush=True)

def pveLoop2():

    '''
    Description:
        function responsible for a player vs AI using Monte Carlo tree search algorithm
    
    '''

    print("PLAYER VS AI")
    print("PLAYER = x")
    print("AI = o")


    gameState = Game([], "x")
    gameState.buildBoard()
    gameState.printGameState()

    while(True):
        if(gameState.currPlayer == "x"):

                line = int(input("Line? "))
                row = int(input("Row? "))
                direction = input("Direction? ")

                if(gameState.move(line, row, direction) == False):
                    print("Invalid Move\n")

                if(gameState.gameStatus == ERROR):
                    print("ERROR LINE 23\n")
            
                if(gameState.gameStatus == DRAW):
                    print("\tResult: Draw\n")
                    gameState.printGameState()
                
                if(gameState.gameStatus == PLAYERX):
                    print("\tResult: Player X Won\n")
                    gameState.printGameState()
                
                if(gameState.gameStatus == PLAYERO):
                    print("\tResult: Player O Won\n")
                    gameState.printGameState()

                gameState.printGameState()

                print(flush=True)

                print("GAME AI IS THINKING...")
                print(flush=True)
                move = monte_carlo_tree_search(gameState)
                print("Move", move, flush = True)
                gameState.move(move[0], move[1], move[2])

                
                print(flush=True)
    


if __name__ == '__main__':

    gameMode = -1
    while (True):
        print("\tMenu")
        print("0 - Exit")
        print("1 - Player vs Player")
        print("2 - Player vs AI Minimax")
        print("3 - Player vs AI Monte Carlo")

        gameMode = int(input("Option: "))

        if(gameMode < 0 or gameMode > 4):
            print("\nInvalid option\nTry again\n")
            continue
        if(gameMode == 0): 
            sys.exit(0)
        if(gameMode == 1): 
            pvpLoop()
        if(gameMode == 2): 
            pveLoop()
        if(gameMode == 3 ):
            pveLoop2()
