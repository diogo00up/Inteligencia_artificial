from cmath import inf
import copy
from gameLogic import *
import math
import numpy as np
from random import randrange

def evalFunction(state):
    '''
        Args:
            state-> current gameState
        Return:
            returns a numerical value calculated by a chosen heuristic
    '''
    k = 10000
    if(state.gameStatus != NOWINNER):
        if(state.gameStatus == DRAW):
            return 0 + k
        if(state.gameStatus == PLAYERX):
            return 1000 + k
        if(state.gameStatus == PLAYERO):
            return -1000 + k

    neigboursXO = state.neighbourKingXO(1)
    return neigboursXO[0] - neigboursXO[1] + state.numberValidMoves("x") - state.numberValidMoves("o") + k



def monte_carlo_tree_search(root):
    '''
    Args:
        root->  current gameState that will be used by the algorithm
    Return:
        returns a chosen gameState that represents the best move for the current situation
    '''
    initial=root            
    current=root            

    novo="o"
    current.filhos=[]
    validMoves(current,novo)   
    
    contador=0
    while(contador<50):

        if(len(current.filhos)==0):        
            if(current.n==0):              
                value=rollout(current,novo)
                while(True):          
                    current.n+=1      
                    current.t+=value
                    if(current==initial):
                        current=initial
                        break


                    current=current.parent

            else:
                if novo=="o":
                    novo="x"
                else : 
                    novo="o"

                current.filhos=[]
                validMoves(current,novo)
                current=current.filhos[0]
               


        else:                   
            biggestnumber=0
            index=0
            
            calculate_ucb1(current)

            for x in range(len(current.filhos)):
                if(current.filhos[x].ucb1>biggestnumber):
                    biggestnumber=current.filhos[x].ucb1
                    index=x
            
            current=current.filhos[index]   
                                             
        contador+=1

    a = chooseNode(current)
    b = chooseNode(initial)
    return a    
  
def calculate_ucb1(current):
    '''
    Args:
        current->  current gameState that will to calculate ucb1
    Descrition:
        calculates the ucb1 value for all current node sons 
    '''
    ln = np.log
    for x in range(len(current.filhos)):
        if(current.filhos[x].n==0):
            current.filhos[x].ucb1=inf
        else:
            current.filhos[x].ucb1=(evalFunction(current.filhos[x]))+2*(math.sqrt(ln( current.filhos[x].t)/ current.filhos[x].n))
       
    
def chooseNode(current):
    '''
    Args:
        current->  current gameState 
    Return:
        returns the son node of current in which value T is the biggest
    '''
    contador = 0
    auxiliar = 1
    for child in current.filhos:
        if(child.t > contador):
            contador = child.t
            auxiliar = child
    #auxiliar.printGameState()
    return auxiliar.mov
    

def rollout(node,novo):
    '''
    Args:
        node->  current gameState
        novo->  represents which player is playing on this state , O or X
    Return:
        returns  heuristic value calculated for the current node
    '''
    current=node
    novo2=novo
    contador=0
    while(contador < 200):
        x=evalFunction(current)
        if(current.gameStatus!=3):  
            return x        
        else:
            if novo2=="o":
                novo2="x"
            else : 
                novo2="o"

            current=choose_random_state(current,novo2)
           
        contador+=1

    return evalFunction(current)


def choose_random_state(root,player):
    '''
    Args:
        root->  current gameState where the tree begins
        player->  represents which player is playing on this state , O or X
    Return:
        returns a new node(GameState)
    '''
    possible=[]    
    nnode=copy.deepcopy(root)
    nnode.depth=root.depth+1
    nnode.currPlayer=player
    nnode.ucb1=0
    nnode.n=0
    nnode.t=0
    nnode.parent=root

    for line in range(len(root.board)):
            for row in range(len(root.board[0])):
                if(root.board[line][row] == root.currPlayer or root.board[line][row] == root.currPlayer.upper()):
                    if([line, row, 'up'] not in root.invalidMoves):
                        array=[line,row,"up"]
                        possible.append(array)

                    if([line, row, 'upRight'] not in root.invalidMoves):
                        array=[line,row,"upRight"]
                        possible.append(array)

                    if([line, row, 'upLeft'] not in root.invalidMoves):
                        array=[line,row,"upLeft"]
                        possible.append(array)

                    if([line, row, 'right'] not in root.invalidMoves):
                        array=[line,row,"right"]
                        possible.append(array)
                    
                    if([line, row, 'left'] not in root.invalidMoves):
                        array=[line,row,"left"]
                        possible.append(array)
                    
                    if([line, row, 'down'] not in root.invalidMoves):
                        array=[line,row,"down"]
                        possible.append(array)

                    if([line, row, 'downRight'] not in root.invalidMoves):
                        array=[line,row,"downRight"]
                        possible.append(array)
                    
                    if([line, row, 'downLeft'] not in root.invalidMoves):
                        array=[line,row,"downLeft"]
                        possible.append(array)

    size=len(possible)         
    y=randrange(size)
    nnode.move(possible[y][0],possible[y][1],possible[y][2])
    return nnode
            
def validMoves(root,player):
    '''
    Args:
        root->  current gameState where the tree begins
        player->  represents which player is playing on this state , O or X
    Description:
        Creates gameSates for all possible moves(plays) in the current game state
    '''
    for line in range(len(root.board)):
        for row in range(len(root.board[0])):
            if(root.board[line][row] == root.currPlayer or root.board[line][row] == root.currPlayer.upper()):
                if([line, row, 'up'] not in root.invalidMoves):
                    nnode=copy.deepcopy(root)
                    nnode.mov = []
                    nnode.depth=root.depth+1
                    nnode.currPlayer=player
                    nnode.n=0
                    nnode.t=0
                    nnode.filhos=[]
                    nnode.parent=root
                    nnode.mov.append(line)
                    nnode.mov.append(row)
                    nnode.mov.append("up")
                    nnode.move(line,row,"up")
                    root.filhos.append(nnode)

                if([line, row, 'upRight'] not in root.invalidMoves):
                    nnode=copy.deepcopy(root)
                    nnode.mov = []
                    nnode.currPlayer=player
                    nnode.depth=root.depth+1
                    nnode.n=0
                    nnode.t=0
                    nnode.filhos=[]
                    nnode.parent=root
                    nnode.mov.append(line)
                    nnode.mov.append(row)
                    nnode.mov.append("upRight")
                    nnode.move(line,row,"upRight")
                    root.filhos.append(nnode)

                if([line, row, 'upLeft'] not in root.invalidMoves):
                    nnode=copy.deepcopy(root)
                    nnode.mov = []
                    nnode.currPlayer=player
                    nnode.depth=root.depth+1
                    nnode.n=0
                    nnode.t=0
                    nnode.filhos=[]
                    nnode.parent=root
                    nnode.mov.append(line)
                    nnode.mov.append(row)
                    nnode.mov.append("upLeft")
                    nnode.move(line,row,"upLeft")
                    root.filhos.append(nnode)

                if([line, row, 'right'] not in root.invalidMoves):
                    nnode=copy.deepcopy(root)
                    nnode.mov = []
                    nnode.depth=root.depth+1
                    nnode.currPlayer=player
                    nnode.n=0
                    nnode.t=0
                    nnode.filhos=[]
                    nnode.parent=root
                    nnode.mov.append(line)
                    nnode.mov.append(row)
                    nnode.mov.append("right")
                    nnode.move(line,row,"right")
                    root.filhos.append(nnode)
                
                if([line, row, 'left'] not in root.invalidMoves):
                    nnode=copy.deepcopy(root)
                    nnode.mov = []
                    nnode.depth=root.depth+1
                    nnode.currPlayer=player
                    nnode.n=0
                    nnode.t=0
                    nnode.filhos=[]
                    nnode.parent=root
                    nnode.mov.append(line)
                    nnode.mov.append(row)
                    nnode.mov.append("left")
                    nnode.move(line,row,"left")
                    root.filhos.append(nnode)
                
                if([line, row, 'down'] not in root.invalidMoves):
                    nnode=copy.deepcopy(root)
                    nnode.mov = []
                    nnode.depth=root.depth+1
                    nnode.currPlayer=player
                    nnode.n=0
                    nnode.t=0
                    nnode.filhos=[]
                    nnode.parent=root
                    nnode.mov.append(line)
                    nnode.mov.append(row)
                    nnode.mov.append("down")
                    nnode.move(line,row,"down")
                    root.filhos.append(nnode)

                if([line, row, 'downRight'] not in root.invalidMoves):
                    nnode=copy.deepcopy(root)
                    nnode.mov = []
                    nnode.depth=root.depth+1
                    nnode.currPlayer=player
                    nnode.n=0
                    nnode.t=0
                    nnode.filhos=[]
                    nnode.parent=root
                    nnode.mov.append(line)
                    nnode.mov.append(row)
                    nnode.mov.append("downRight")
                    nnode.move(line,row,"downRight")
                    root.filhos.append(nnode)
                
                
                if([line, row, 'downLeft'] not in root.invalidMoves):
                    nnode=copy.deepcopy(root)
                    nnode.mov = []
                    nnode.depth=root.depth+1
                    nnode.depth=root.depth+1
                    nnode.currPlayer=player
                    nnode.n=0
                    nnode.t=0
                    nnode.filhos=[]
                    nnode.parent=root
                    nnode.mov.append(line)
                    nnode.mov.append(row)
                    nnode.mov.append("downLeft")
                    nnode.move(line,row,"downLeft")
                    root.filhos.append(nnode)
                        
    

