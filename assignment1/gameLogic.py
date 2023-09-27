from colorama import Fore, Back, Style
import math
import random
from copy import deepcopy

ERROR = -1
DRAW = 0
PLAYERX = 1
PLAYERO = 2
NOWINNER = 3

class Game:

    def __init__(self, board, currentPlayer):
        self.board = board
        self.connectedTable = []
        self.currPlayer = currentPlayer
        self.gameStatus = 3

        ###here
        self.parent=None
        self.filhos=[]
        self.ucb1=0
        self.t=0
        self.n=0  #numero de visitas
        self.mov=[]
        self.depth=0
        self.invalidMoves = []

    def toString(self):
        str = ""
        for y in range(len(self.board)):
                for x in range(len(self.board[0])):
                    str += self.board[y][x]

        str += self.currPlayer

        return str

    def addfilho(self,node):
        '''
        Args:
            self-> current node
            node > node to be added to a vector
        Description:
             Appends a node to son vector of self node

        '''
        self.filhos.append(node)
        
    def printGameState(self):
        '''
        Args:
            self-> current node
        Description:
            Prints the current GameState, this is the game board

        '''
        print("  |", end = " ")
        if(len(self.board[0]) <= 10):
            for x in range(len(self.board[0])):
                print(x, end = " ")

            print("\n")

            for y in range(len(self.board)):
                print(y, "|", end = " ")
                for x in range(len(self.board[0])):

                    if(self.board[y][x] == '.'):
                        print(Style.RESET_ALL, end = "")
                    elif(self.board[y][x] == 'x' or self.board[y][x] == 'X'):
                        print(Fore.RED, end = "")
                    elif(self.board[y][x] == 'o' or self.board[y][x] == 'O'):
                        print(Fore.BLUE, end = "")
                    
                    print (self.board[y][x], end = " ")
                print("\n")
                print(Style.RESET_ALL, end = "")

            print("Player " + self.currPlayer + " turn \n")
            print("Invalid moves ", self.invalidMoves)
        else:
            print("To do later")

    def buildBoard(self):
        '''
        Args:
            self-> current node
        Description:
            Constructs the game board

        '''
        '''
        Fix this later
        '''
        lines = 9
        rows = 10

        connectBoard = []
        newBoard = []
        for _ in range(lines):
            line = []
            line1 = []
            for _ in range(rows):
                line.append('.')
                line1.append(False)
            newBoard.append(line)
            connectBoard.append(line1)

        elem = 'x'
        for line in range(2, 7):

            if( newBoard[line-1][2] == 'x'): elem = 'o'
            else: elem = 'x'

            for row in range(2, 8):
                newBoard[line][row] = elem
                
                if(line == 4 and (row == 4 or row == 5)):
                    if(elem == 'x'): newBoard[line][row] = 'X'
                    else: newBoard[line][row] = 'O'

                elem = 'x' if elem != 'x' else 'o'

        self.board = newBoard
        self.connectedTable = connectBoard

    def buildMiniBoard(self):
        '''
        Args:
            self-> current node
        Description:
            Constructs a smaller game Board than the normal sized one

        '''
        lines = 7
        rows = 8
        
        connectBoard = []
        newBoard = []
        for _ in range(lines):
            line = []
            line1 = []
            for _ in range(rows):
                line.append('.')
                line1.append(False)
            newBoard.append(line)
            connectBoard.append(line1)

        elem = 'x'
        for line in range(2, 5):

            if( newBoard[line-1][2] == 'x'): elem = 'o'
            else: elem = 'x'

            for row in range(2, 6):
                newBoard[line][row] = elem
                
                if(line == 3 and (row == 3 or row == 4)):
                    if(elem == 'x'): newBoard[line][row] = 'X'
                    else: newBoard[line][row] = 'O'

                elem = 'x' if elem != 'x' else 'o'

        self.board = newBoard
        self.connectedTable = connectBoard

    '''
        Returns False if the move selected is invalid
    '''
    def move(self, line, row, direction):
        '''
        Args:
            self-> current node
            line-> line index that was chosen
            row-> row index that was chosen
            direction-> direction to be moved to
        Description:
            Responsible for moving the board pieces around the board

        '''

        if(line < 0 or line > len(self.board) -1 or row < 0 or row > len(self.board[0]) - 1):
            print("Indexes out of range\n")
            return False

        #check that the piece at this position is of the sam type as currPlayer
        if(self.board[line][row] == '.'): 
            return False
        elif(self.currPlayer == 'x'):
            if(self.board[line][row] != 'x' and self.board[line][row] != 'X'): 
                return False
        elif(self.currPlayer == 'o'):
            if(self.board[line][row] != 'o' and self.board[line][row] != 'O'): 
                return False

        if([line, row, direction] in self.invalidMoves):
            return False

        self.invalidMoves = []

        replaced = self.board[line][row]
        self.board[line][row] = '.'
        self.movePiece(line, row, direction, replaced)
        
        self.nextPlayer()
        
        self.gameEnded()
        
        self.setInvalidMoves(line, row)

        return True

    def setInvalidMoves(self, line, row):
        '''
        Args:
            self-> current node
            line > line  to start the search of invalid moves
            row -> column to start the search of invalid moves
        Description:
            Gives the game a set of invalid moves

        '''
        for direction in ['upLeft', 'up', 'upRight', 'left', 'right', 'downLeft', 'down', 'downRight']:
            self.setInvalidMovesCheckLine(line, row, direction)

    def setInvalidMovesCheckLine(self, line, row, direction):
        '''
        Args:
            self-> current node
            line > line  to start the search of invalid moves
            row -> column to start the search of invalid moves
            direction -> direction that the piece must move

        Description:
            Check if the surrounding squares of the current chosen piece are available 

        '''
        match direction:
            case 'up':
                line = line - 1
            case 'down':
                line = line + 1            
            case 'right':
                row = row + 1
            case 'left':
                row = row - 1
            case 'upRight':
                line = line - 1
                row = row + 1
            case 'upLeft':
                line = line - 1
                row = row - 1
            case 'downLeft':
                line = line + 1
                row = row - 1
            case 'downRight':
                line = line + 1
                row = row + 1
        if (line >= 0 and row >= 0 and line < len(self.board) and row < len(self.board[0])):
            if(self.board[line][row] != '.'):
                if(self.board[line][row] == self.currPlayer or self.board[line][row].lower() == self.currPlayer):
                    self.invalidMoves.append([line, row, self.invertDirection(direction)])
                    self.setInvalidMovesCheckLine(line, row, direction)
                else:
                    self.setInvalidMovesCheckLine(line, row, direction)

    def movePiece(self, line, row, direction, piece):
        '''
        Args:
            self-> current node
            line > line  to start the search of invalid moves
            row -> column to start the search of invalid moves
            direction -> direction that the piece must move
            piece -> piece to be moved

        Description:
           pushes the pieces on a specified direction and poisition

        '''

        match direction:
            case 'up':
                line = line - 1
            case 'down':
                line = line + 1            
            case 'right':
                row = row + 1
            case 'left':
                row = row - 1
            case 'upRight':
                line = line - 1
                row = row + 1
            case 'upLeft':
                line = line - 1
                row = row - 1
            case 'downLeft':
                line = line + 1
                row = row - 1
            case 'downRight':
                line = line + 1
                row = row + 1
                
        if (line >= 0 and row >= 0 and line < len(self.board) and row < len(self.board[0])):
            replaced = self.board[line][row]
            self.board[line][row] = piece

            #if(self.board[line][row] != self.currPlayer and self.board[line][row] != self.currPlayer.lower()):
            #    self.invalidMoves.append([line, row, self.invertDirection(direction)])
            
            if(replaced == '.'): return True
            
            return self.movePiece(line, row, direction, replaced)
        else:
            return False

    def invertDirection(self, direction):
        '''
        Args:
            self-> current node
            direction -> direction that the piece wans to move to

       Return:
            Returns an invalid direction for a piece movement
            

        '''
        match direction:
            case 'up':
                return 'down'
            case 'down':
                return 'up'          
            case 'right':
                return 'left'
            case 'left':
                return 'right'
            case 'upRight':
                return 'downLeft'
            case 'upLeft':
                return 'downRight'
            case 'downLeft':
                return 'upRight'
            case 'downRight':
                return 'upLeft'

        return '---'
    
    '''
    Removes pieces where disconnected = False
    '''
    def removeDisconnectedPieces(self):
        '''
        Args:
            self-> current node
        Description:
            Removes disconect pieces from the gameBoard according to the game rules
            
        '''
        
        for line in range(len(self.board)):
            for row in range(len(self.board[0])):
                if(self.connectedTable[line][row] == False and self.board[line][row] != '.'):
                    self.board[line][row] = '.'

    '''
    returns the number of pieces connected to the starting postion
    '''
    def bfs(self, startLine, startRow):
        '''
        Args:
            self-> current node
            startLine -> starting line position of the bfs
            startLine -> starting column position of the bfs
        Return:
            returns number of pieces conected to a startLine and startRow coordinates
            
        '''
        queue = [(startLine, startRow)]
        piecesConnected = 0

        while(len(queue) > 0):
            pos = queue.pop()
            if(self.connectedTable[pos[0]][pos[1]] == True): continue

            piecesConnected += 1

            self.connectedTable[pos[0]][pos[1]] = True

            x = pos[1]
            y = pos[0]

            if( y - 1 >= 0):
                if x - 1 >= 0 and self.board[y-1][x-1] != '.':
                    queue.append((y-1, x-1))

                if(self.board[y-1][x] != '.'):
                    queue.append((y-1, x))
                
                if x + 1 < len(self.board[0]) and self.board[y-1][x+1] != '.' :
                    queue.append((y-1, x+1))
            
            if( x - 1 >= 0 and self.board[y][x-1] != '.'): 
                queue.append((y, x-1))
            
            if( x + 1 < len(self.board[0]) and self.board[y][x+1] != '.'):
                queue.append((y, x + 1))
    
            if( y + 1 < len(self.board)):
                if x - 1 >= 0 and self.board[y+1][x-1] != '.':
                    queue.append((y+1, x-1))

                if self.board[y+1][x] != '.' :
                    queue.append((y+1, x))
                
                if x + 1 < len(self.board[0]) and self.board[y+1][x+1] != '.':
                    queue.append((y+1, x+1))

        return piecesConnected

    '''
    returns     -1 on error
                0 on draw
                1 on player X victory
                2 on player y victory
                3 on no winner
    '''
    def gameEnded(self):
        '''
        Args:
            self-> current node

        Description:
            returns the game state which will be reponsible to atributte a win,draw or lost
            
        '''
        kingXline = -1
        kingXrow = -1
        kingOline = -1
        kingOrow = -1

        '''
            Find kings indexes
        '''
        for line in range(len(self.board)):
            for row in range(len(self.board[0])):
                self.connectedTable[line][row] = False
                if(self.board[line][row] == 'O'):
                    kingOline = line
                    kingOrow = row
                elif(self.board[line][row] == 'X'):
                    kingXline = line
                    kingXrow = row

        '''
            No king found
            Error
        '''
        if kingOline == -1 and kingXline == -1:
            self.gameStatus = ERROR
            return ERROR

        '''
            king O pushed off board
        '''
        if kingOline == -1:
            self.gameStatus = PLAYERX
            return PLAYERX #jogador 1 ganhou
        
        '''
            king X pushed off board
        '''
        if kingXline == -1:
            self.gameStatus = PLAYERO
            return PLAYERO #jogador 2 ganhou

        '''
            Bfs search starting with KingX coords
        '''
       
        connectedKingX = self.bfs(kingXline, kingXrow)

        '''
            kings are separated
        '''
        if self.connectedTable[kingOline][kingOrow] == False:
            '''
                Bfs search starting with KingO coords
            '''
            connectedKingO = self.bfs(kingOline  , kingOrow)

            self.removeDisconnectedPieces()

            numberOfXpawns = 0
            numberOfOpawns = 0
            for line in range(len(self.board)):
                for row in range(len(self.board[0])):
                    self.connectedTable[line][row] = False
                    if(self.board[line][row] == 'x'):
                        numberOfXpawns += 1
                    elif(self.board[line][row] == 'o'):
                        numberOfOpawns += 1

            #As kings are separated, calculate winner by
            if(connectedKingX > connectedKingO):
                self.gameStatus = PLAYERX
                return PLAYERX
            elif(connectedKingX < connectedKingO):
                self.gameStatus = PLAYERO
                return PLAYERO
            else:
                if(numberOfXpawns > numberOfOpawns):
                    self.gameStatus = PLAYERX
                    return PLAYERX
                elif(numberOfOpawns > numberOfXpawns):
                    self.gameStatus = PLAYERO
                    return PLAYERO
                self.gameStatus = DRAW
                return DRAW


        self.removeDisconnectedPieces()

        numberOfXpawns = 0
        numberOfOpawns = 0
        for line in range(len(self.board)):
            for row in range(len(self.board[0])):
                self.connectedTable[line][row] = False
                if(self.board[line][row] == 'x'):
                    numberOfXpawns += 1
                elif(self.board[line][row] == 'o'):
                    numberOfOpawns += 1

        if(numberOfOpawns == 0 and numberOfXpawns == 0):
            self.gameStatus = DRAW
            return DRAW
        elif(numberOfOpawns == 0):
            self.gameStatus = PLAYERX
            return PLAYERX
        elif(numberOfXpawns == 0):
            self.gameStatus = PLAYERO
            return PLAYERO

        self.gameStatus = NOWINNER
        return NOWINNER
            
    def nextPlayer(self):
        '''
        Args:
            self-> current node
        Description:
            Choses what player must play at the next time
            
            
        '''
        if(self.currPlayer == "x"): 
            self.currPlayer = "o"
        else:
            self.currPlayer = "x"

    def distance(self, x, y, xx, yy):
        '''
        Args:
            self-> current node
            x ->  line index of the the first piece
            y ->  column index of the first piece
            xx ->  line index of the the second piece
            y y->  column index of the second piece
        Return:
            returns the distance between 2 game pieces
            
        '''
        return math.sqrt((x-xx)**2 + (y-yy)**2)

    def neighbourKingXO(self, distanceRatio):
        '''
        Args:
            self-> current node
            distanceRatio->  Factor that is used calculate the value of the game pieces
        Return:
            returns the value of the pieces around KingX and KingO
            
        '''

        neighbourKingX = 0
        neighbourKingO = 0

        '''
            Find kings indexes
        '''
        for line in range(len(self.board)):
            for row in range(len(self.board[0])):
                self.connectedTable[line][row] = False
                if(self.board[line][row] == 'O'):
                    kingOline = line
                    kingOrow = row
                if(self.board[line][row] == 'X'):
                    kingXline = line
                    kingXrow = row

        for line in range(kingXline-2, kingXline+2, 1):
            for row in range(kingXrow-2, kingXrow+2, 1):
                if(line < 0 or row < 0 or line > len(self.board) - 1 or row > len(self.board[0])-1):
                    continue
                if(self.board[line][row] == "x"):
                    neighbourKingX += (1/self.distance(line, row, kingXline, kingXrow)) * distanceRatio


        for line in range(kingOline-1, kingOline+1, 1):
            for row in range(kingOrow-1, kingOrow+1, 1):
                if(line < 0 or row < 0 or line > len(self.board) - 1 or row > len(self.board[0])-1):
                    continue
                if(self.board[line][row] == "o"):
                    neighbourKingO += (1/self.distance(line, row, kingOline, kingOrow)) * distanceRatio

        return [neighbourKingX, neighbourKingO]

    def validMoves(self):
        '''
        Args:
            self-> current node
       
        Return:
            returns a vector with all possible moves for the current state
            
        '''
        moves = []
        for line in range(len(self.board)):
            for row in range(len(self.board[0])):
                if(self.board[line][row] == self.currPlayer or self.board[line][row] == self.currPlayer.upper()):

                    moves.append([line, row, "up"])
                    moves.append([line, row, "upRight"])
                    moves.append([line, row, "upLeft"])
                    moves.append([line, row, "right"])
                    moves.append([line, row, "left"])
                    moves.append([line, row, "down"]) 
                    moves.append([line, row, "downRight"])
                    moves.append([line, row, "downLeft"])

        for move in self.invalidMoves:
            moves.remove(move) if move in moves else moves
        return moves  ##linha coluna direcao

    def numberValidMoves(self, player):
        '''
        Args:
            self-> current node
            player->  current player
          
        Return:
            returns the number of moves that currentplayer can do
            
        '''
        if(player == self.currPlayer):
            return len(self.validMoves())

        self.nextPlayer()
        moves = len(self.validMoves())
        self.nextPlayer()

        return moves

    def randomMove(self):
        '''
        Args:
            self-> current node
        Return:
            returns a radom move
            
        '''
        move = random.choice(self.validMoves())
        return move