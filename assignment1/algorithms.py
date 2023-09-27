import math
from gameLogic import *
from copy import deepcopy

def minimax(heuristicValues, state, depth = 10, alpha = -math.inf, beta = math.inf):
    """
        Minimax algorithm
        Args:
            heuristicValues -> list of heuristic values
            state -> current game state to expand
            depth -> depth of the algorithm
            alpha -> alpha value
            beta -> beta value
        Return:
            returns the evaluation and the best move
    """
    if depth == 0 or state.gameStatus != NOWINNER: 
        if(state.currPlayer == "x"):
            return evaluationFunction(state, heuristicValues[0], heuristicValues[1], heuristicValues[2], heuristicValues[3], heuristicValues[4], heuristicValues[5], heuristicValues[6]), []
        else:
            return evaluationFunction(state, heuristicValues[0], heuristicValues[1], heuristicValues[2], heuristicValues[3], heuristicValues[4], heuristicValues[5], heuristicValues[6]), []

    bestMove = []
    validMoves = state.validMoves()
    if state.currPlayer == "x":
        maxEval = -math.inf
        l = []
        for i in range(len(validMoves)):
            move = validMoves[i]
            childState = deepcopy(state)
            if(childState.move(move[0], move[1], move[2]) == False): continue
            
            l.append([childState, evaluationFunction(state, heuristicValues[0], heuristicValues[1], heuristicValues[2], heuristicValues[3], heuristicValues[4], heuristicValues[5], heuristicValues[6]), move])

        sameEvalMoves = []
        for elem in l:
            evaluation, bestReturnedMove = minimax(heuristicValues, elem[0], depth-1, alpha , beta)

            if(evaluation > maxEval):
                maxEval = evaluation
                bestMove = elem[2]
                sameEvalMoves = [elem[2]]
            elif(maxEval == evaluation):
                sameEvalMoves.append(elem[2])
                bestMove = elem[2]
            alpha = max(alpha, maxEval)
            if beta <= alpha: 
                break
        bestMove = random.choice(sameEvalMoves)
        return maxEval, bestMove
    
    minEval = math.inf

    l = []
    for i in range(len(validMoves)):
        move = validMoves[i]
        childState = deepcopy(state)
        if(childState.move(move[0], move[1], move[2]) == False): continue
        l.append([childState, evaluationFunction(state, heuristicValues[0], heuristicValues[1], heuristicValues[2], heuristicValues[3], heuristicValues[4], heuristicValues[5], heuristicValues[6]), move])
    for elem in l:

        evaluation, bestReturnedMove = minimax(heuristicValues, elem[0], depth-1, alpha , beta)

        if(evaluation < minEval):
            minEval = evaluation
            bestMove = elem[2]
        elif(evaluation == minEval):
            if(random.uniform(0, 1) > 0.5):
                bestMove = elem[2]

        beta = min(beta, minEval)
        if beta <= alpha: 
            break
    return minEval, bestMove


def evaluationFunction(gameState, value1, value2, value3, value4, value5, value6, value7):
    """
        Function that evaluates a game state based on the given values
        Args:
            gameState -> game state to evaluate
            value1 -> float value
            value2 -> float value
            value3 -> float value
            value4 -> float value
            value5 -> float value
            value6 -> float value
            value7 -> float value
        Return:
            returns the value of the game state
    """
    if(gameState.gameStatus != NOWINNER):
        if(gameState.gameStatus == DRAW):
            return 0
        if(gameState.gameStatus == PLAYERX):
            return math.inf
        if(gameState.gameStatus == PLAYERO):
            return -math.inf
    if(gameState.currPlayer == "x"):
        return value1 * (value5 * gameState.numberValidMoves("x") - (1-value5) * gameState.numberValidMoves("o")) + value2 * (value6 * gameState.neighbourKingXO(value3)[0] - (1-value6) * gameState.neighbourKingXO(value4)[1]) + value7 * 1

    return value1 * ((1 - value5) * gameState.numberValidMoves("x") - value5 * gameState.numberValidMoves("o")) + value2 * ((1 - value6) * gameState.neighbourKingXO(value3)[0] - value6 * gameState.neighbourKingXO(value4)[1]) + value7 * (-1)

