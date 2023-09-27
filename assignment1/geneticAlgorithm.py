import math
import time
import random
from datetime import date, datetime
from gameLogic import *

def playGame(heuristicValues1, heuristicValues2):
    """
        Plays a game between two minimax players
        Args:
            heuristicValues1 -> list of float values used to evaluate a game state
            heuristicValues2 -> list of float values used to evaluate a game state
        Return:
            returns -1 on error, 0 on draw, 1 on player x winning, 2 on player o winning
    """
    game = Game([], "x")
    game.buildMiniBoard()

    while(game.gameStatus == NOWINNER):
        #game.printGameState()
        print(flush=True)

        evaluation, bestMove = minimax(heuristicValues1, heuristicValues2, game, 3)

        print(bestMove, evaluation, flush=True)
        game.move(bestMove[0], bestMove[1], bestMove[2])

    #game.printGameState()

    print("Game Ended ", game.gameStatus)

    if(game.gameStatus == PLAYERX): return 1
    if(game.gameStatus == PLAYERO): return 2
    if(game.gameStatus == DRAW): return 0

    return ERROR

def optimizeHeuristic():
    """
        Perfroms a 5 games using various heuristic values, selecting the winner heuristics in the end 
        and creating a new set of heuristic values, repeating theis process 5 times
        Args: None
        Return: None
    """

    population = generateInitialPopulation()
    populationResults = [0 for _ in range(len(population))]
    iterationNumber = 5



    for z in range(iterationNumber):
        f = open("demofile4.txt", "a")
        f.write("Iteration " + str(z) + "\n")
        f.write(str(population))
        f.write("\n")

        print("Iteration ", z)
        for a in range(5):
            print("Run ", a, "\n\n")
            for i in range(round(len(population)/2)):
                print("Starting ", i, population[i], population[i + round(len(population)/2)],flush=True)
                f.write("Starting " + str(i) + " " +  str(population[i]) + " " + str(population[i + round(len(population)/2)]) + "\n")
                time1 = time.time()
                res = playGame(population[i], population[i + round(len(population)/2)])
                time2 = time.time()
                f.write(str(time2-time1) + "\n")
                if(res == 1):
                    populationResults[i] += 1
                if(res == 2):
                    populationResults[i + round(len(population)/2)] += 1
                if(res == 0):
                    print("Draw", flush = True)
                if(res == ERROR):
                    print("Error occured ", i, i + round(len(population))/2, flush=True)
                    f.close()
                    return ERROR
        print(populationResults, flush=True)
        f.write(str(populationResults) + "\n")

        winners = selectWinners(populationResults, population)
        print("Winners " + str(winners) + "\n")
        print("Winners ")
        for w in winners:
            print(w)
        if(z == iterationNumber - 1):
            f.close()
            return winners

        population = createNewPopulation(winners, 10)
        random.shuffle(population)
        print("newPopulation ")
        for w in population:
            print(w)
        populationResults = [0 for _ in range(len(population))]
        f.close()

def selectWinners(results, population):
    """
        Selects and returns 5 heuristics values which had the most wins 
        Args:
            results -> list of values that depict the results between heuristic n and heusristic n + len(population)/2
            population -> list of heuristic values
        Return:
            returns a list of heuristic values which had the most number of wins
    """
    goodIndividuals = []
    for i in range(int(len(results)/2)):
        if (results[i] > results[i+int(len(results)/2)]):
            goodIndividuals.append(population[i])
        elif(results[i] < results[i+int(len(results)/2)]):
            goodIndividuals.append(population[i+int(len(results)/2)])
        else:
            goodIndividuals.append(sameResultsHeuristic(population[i], population[i+int(len(population)/2)]))

    return goodIndividuals

def createNewPopulation(population, expectedPopSize):
    """
        Generates a list containning lists of heuristic values based on a given population
        Args:
            population -> list of heuristic values
            expectedPopSize -> expected number of heuristic value lists
        Returns:
            returns a list of heuristic values
    """
    res = deepcopy(population)

    mutationFactor = 0.2

    while(len(res) != expectedPopSize):
        [x, y] =  random.sample(population, 2)
        res.append(breed(x, y))
    
    print("before mutation ")
    for r in res:
        print(r)
    for i in range(len(res)):
        if mutationFactor > random.uniform(0,1):
            print('Mutate')
            res[i] = mutateHeuristic(res[i])

    return res

def mutateHeuristic(h1):
    """
        Mutates a list of heuristic values
        Args:
            h1 -> list of heuristic values
        Return:
            returns a list of mutated heuristiv values
    """
    h = deepcopy(h1)
    
    for i in range(len(h)):
        h[i] = h[i] + random.uniform(-0.15, 0.15)
    
    return h

def breed(x, y):
    """
        Produces a list containning heuristic values based on the parents
        Args:
            x -> list of heuristic values
            y -> list of heuristic values
        Return:
            returns a list of heuristic values based on the arguments given
    """
    if(x == y):
        print("x == y")
        print(x, y)
        return -1

    newChild = []
    for i in range(len(x)):
        if x[i] > y[i]:
            childWeight = random.uniform(y[i] - y[i]*.05, x[i] + x[i]*.05)
        else:
            childWeight = random.uniform(x[i] - x[i]*.05, y[i] + y[i]*.05)

        newChild.append(childWeight)
    
    return newChild

def sameResultsHeuristic(pop1, pop2):
    """
        Args:
            pop1 -> list of heuristic values
            pop2 -> list of heuristic values
        Return:
            returns a list of heuristic values that is the average of the arguments
    """
    res = []
    for i in range(len(pop1)):
        res.append((pop1[i] + pop2[i]) / 2)
    return res

def generateInitialPopulation():
    """
        Function that generates the inital population for the genetic algorithm
        Args: None
        Return:
            returns a list of lists of heuristic values
    """
    populationSize = 10
    #vals = [[random.uniform(-1, 1) for _ in range(7)] for _ in range(populationSize)]
    vals = [[1, 0, 0, 0, 1, 0, 0], 
            [1, 0, 0, 0, 0.5, 0, 0], 
            [0, 1, 1, 0, 0, 1, 0], 
            [0, 1, 1, 1, 0, 0.5, 0],
            [1, 0, 0, 0, 0.7, 0, 0],
            [0, 1, 1, 1, 0, 0.7, 0],
            [1, 1, 1, 1, 0.7, 0.7, 0],
            [0.5, 1, 1, 1, 0.5, 0.5, 1],
            [1, 0.5, 1, 1, 0.5, 0.5, 1],
            [0.7, 0.4, 0.3, 0.3, 0.7, 0.6, 1]
            ]
    return vals

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

def minimax(heuristicValues1, heuristicValues2, state, depth = 3, alpha = -math.inf, beta = math.inf):
    """
        Version of the minimax algorithm that uses different heuristic values
        Args:
            heuristicValues1 -> list of heuristic values
            heuristicValues2 -> list of heuristic values
            state -> current game state to expand
            depth -> depth of the algorithm
            alpha -> alpha value
            beta -> beta value
        Return:
            returns the evaluation and the best move
    """
    if depth == 0 or state.gameStatus != NOWINNER: 
        if(state.currPlayer == "x"):
            return evaluationFunction(state, heuristicValues1[0], heuristicValues1[1], heuristicValues1[2], heuristicValues1[3], heuristicValues1[4], heuristicValues1[5], heuristicValues1[6]), []
        else:
            return evaluationFunction(state, heuristicValues2[0], heuristicValues2[1], heuristicValues2[2], heuristicValues2[3], heuristicValues2[4], heuristicValues2[5], heuristicValues2[6]), []

    bestMove = []
    validMoves = state.validMoves()
    if state.currPlayer == "x":
        maxEval = -math.inf
        l = []
        for i in range(len(validMoves)):
            move = validMoves[i]
            childState = deepcopy(state)
            if(childState.move(move[0], move[1], move[2]) == False): continue
            
            l.append([childState, evaluationFunction(state, heuristicValues1[0], heuristicValues1[1], heuristicValues1[2], heuristicValues1[3], heuristicValues1[4], heuristicValues1[5], heuristicValues1[6]), move])

        sameEvalMoves = []
        for elem in l:
            evaluation, bestReturnedMove = minimax(heuristicValues1, heuristicValues2, elem[0], depth-1, alpha , beta)

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
        l.append([childState, evaluationFunction(state, heuristicValues2[0], heuristicValues2[1], heuristicValues2[2], heuristicValues2[3], heuristicValues2[4], heuristicValues2[5], heuristicValues2[6]), move])
    for elem in l:

        evaluation, bestReturnedMove = minimax(heuristicValues1, heuristicValues2, elem[0], depth-1, alpha , beta)

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

if __name__ == "__main__":
    random.seed(datetime.now().timestamp())

    f = open("demofile4.txt", "a")
    a = datetime.now()
    f.write(str(a) + "\n")
    f.close()
    optimizeHeuristic()

    