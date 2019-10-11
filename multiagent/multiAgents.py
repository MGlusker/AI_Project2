# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import searchAgents
import search

from game import Agent


class ReflexAgent(Agent):

    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):


        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        foodList = newFood.asList()
        foodDistances = []
        finalScore = 0.0

        # find the manhattan distance to each pellet of food
        for food in foodList:    
            foodDistances.append(manhattanDistance(successorGameState.getPacmanPosition(), food))

        # if there's no food left in the game
        if(len(foodDistances) == 0): 
          # if the next state will result in there being 0 pellets of food left, take that move
          return finalScore + 100000000
         
        else:
          # get the closest food and scale it up to make it more desireable
          closestFoodDistance = min(foodDistances) 
          closestFoodScore = (1.0/closestFoodDistance) * 500.0


        #creates a list of distances to ghosts
        distanceToGhosts = []
        for ghost in newGhostStates:
          distanceToGhosts.append(manhattanDistance(successorGameState.getPacmanPosition(), ghost.getPosition()))

        # manhattan distance to the closest ghost
        closestGhostDistance = min(distanceToGhosts)
  

        # if pacman is vulnerable to ghosts or is about to become vulnerable (arbitrary cut off is 3 seconds)
        if(min(newScaredTimes) <= 3):

          # if the next spot is  food, GOOD, increase score
          if(len(newFood.asList()) < len(currentGameState.getFood().asList())):
            finalScore += 1000


          # if pacman is close to a ghost, BAD, decrement score 
          if(closestGhostDistance <= 3):
            if(closestGhostDistance == 0):
              finalScore -= float("inf")
            if(closestGhostDistance == 1):
              finalScore -= 10000
            if(closestGhostDistance == 2):
              finalScore -= 8000
            if(closestGhostDistance == 3):
              finalScore -= 7000

          # otherwise pacman is at least 4 spaces away
          else:
            # so reward the closest food spot 
            finalScore += closestFoodScore

        # otherwise pacman can go wherever, so go straight for food without care for ghosts
        else:
          finalScore += closestFoodScore
          # if the next spot is  food, GOOD, increase score
          if(len(newFood.asList()) < len(currentGameState.getFood().asList())):
            finalScore += 1000

        return finalScore 

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """
    

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        


class MinimaxAgent(MultiAgentSearchAgent):

    """
      Your minimax agent (question 2)
    """
  

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """


        #It's necessarily pacman's turn cause this is at the root 

        pacmanSuccessors = [] #list of GameStates
        pacmanSuccessorsEvalScores = [] #list of GameStates returned scores

        pacmanLegalActions = gameState.getLegalActions(self.index)

        for action in pacmanLegalActions:
          pacmanSuccessors.append(gameState.generateSuccessor(self.index, action))
        
        for child in pacmanSuccessors:
          pacmanSuccessorsEvalScores.append(self.getActionRecursiveHelper(child, 1))

        return pacmanLegalActions[pacmanSuccessorsEvalScores.index(max(pacmanSuccessorsEvalScores))]
     


    def getActionRecursiveHelper(self, gameState, depthCounter):

      numAgents = gameState.getNumAgents()

      #cutoff test
      if((self.depth*numAgents) == depthCounter):
        return self.evaluationFunction(gameState)

      #implement a terminal test
      if(gameState.isWin() ==True or gameState.isLose() == True):
        return self.evaluationFunction(gameState)

      # When it's pacman's turn
      if((depthCounter%numAgents) == self.index): 

        pacmanSuccessors = [] #list of GameStates
        pacmanSuccessorsEvalScores = [] #list of GameStates returned scores

        pacmanLegalActions = gameState.getLegalActions(self.index)

        for action in pacmanLegalActions:
          pacmanSuccessors.append(gameState.generateSuccessor(self.index, action))

        for child in pacmanSuccessors:
          pacmanSuccessorsEvalScores.append(self.getActionRecursiveHelper(child, depthCounter+1))

        return max(pacmanSuccessorsEvalScores)


      #It's a ghost turn
      else: 

        ghostNumber = (depthCounter%numAgents) #which ghost is it?
        ghostSuccessors = [] #list of GameStates
        ghostSuccessorsEvalScores = [] #list of GameStates returned scores

        ghostLegalActions = gameState.getLegalActions(ghostNumber)

        for action in ghostLegalActions:
          ghostSuccessors.append(gameState.generateSuccessor(ghostNumber, action))

        for child in ghostSuccessors:
          ghostSuccessorsEvalScores.append(self.getActionRecursiveHelper(child, depthCounter+1))
      
        return min(ghostSuccessorsEvalScores)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """


        #It's necessarily pacman's turn cause this is at the root 

        pacmanSuccessors = [] #list of GameStates
        pacmanSuccessorsEvalScores = [] #list of GameStates returned scores
        alpha = -float('Inf')
        beta = float('Inf')
        v = -float('Inf')

        pacmanLegalActions = gameState.getLegalActions(self.index)

        for action in pacmanLegalActions:
          pacmanSuccessors.append(gameState.generateSuccessor(self.index, action))
        
        for child in pacmanSuccessors:
          v = max([v, self.minRecursiveHelper(child, 1, 1, alpha, beta)])
          pacmanSuccessorsEvalScores.append(v)

          if(v > beta):
            break

          alpha = max([alpha, v])


        return pacmanLegalActions[pacmanSuccessorsEvalScores.index(max(pacmanSuccessorsEvalScores))]
     


    def maxRecursiveHelper(self, gameState, depthCounter, ghostNumber, alpha, beta):

      numAgents = gameState.getNumAgents()
      v = -float('Inf')

      #cutoff test
      if((self.depth*numAgents) == depthCounter):

        return self.evaluationFunction(gameState)

      #implement a terminal test
      if(gameState.isWin() == True or gameState.isLose() == True):

        return self.evaluationFunction(gameState)

      pacmanSuccessors = [] #list of GameStates
      pacmanSuccessorsEvalScores = [] #list of GameStates returned scores

      pacmanLegalActions = gameState.getLegalActions(self.index)


      for action in pacmanLegalActions:
        child = gameState.generateSuccessor(self.index, action)

      
        v = max([v, self.minRecursiveHelper(child, depthCounter+1, ghostNumber, alpha, beta)])

        if(v > beta):
          return v

        alpha = max([alpha, v])

        
      return v


    def minRecursiveHelper(self, gameState, depthCounter, ghostNumber, alpha, beta):

      numAgents = gameState.getNumAgents()
      v = float('Inf')

      #cutoff test
      if((self.depth*numAgents) == depthCounter):

        return self.evaluationFunction(gameState)

      #implement a terminal test
      if(gameState.isWin() ==True or gameState.isLose() == True):

        return self.evaluationFunction(gameState)


      ghostSuccessors = [] #list of GameStates
      ghostSuccessorsEvalScores = [] #list of GameStates returned scores

      ghostLegalActions = gameState.getLegalActions(ghostNumber)

      for action in ghostLegalActions:
        child = gameState.generateSuccessor(ghostNumber, action)

        # When it's pacman's turn
        if ghostNumber == numAgents-1:
        #if((depthCounter%numAgents) == self.index):

          v = min([v, self.maxRecursiveHelper(child, depthCounter+1, 1, alpha, beta)])


        # otherwise it's the next ghosts turn
        else:
          v = min([v, self.minRecursiveHelper(child, depthCounter+1, ghostNumber+1, alpha, beta)])
        

        if(v < alpha):
          return v
      
        beta = min([beta, v])
      
      return v
      
        
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing -uniformly at random from their
          legal moves.
        """

        #It's necessarily pacman's turn cause this is at the root 

        pacmanSuccessors = [] #list of GameStates
        pacmanSuccessorsEvalScores = [] #list of GameStates returned scores

        pacmanLegalActions = gameState.getLegalActions(self.index)

        for action in pacmanLegalActions:
          pacmanSuccessors.append(gameState.generateSuccessor(self.index, action))
        
        for child in pacmanSuccessors:
          pacmanSuccessorsEvalScores.append(self.getActionRecursiveHelper(child, 1))

        return pacmanLegalActions[pacmanSuccessorsEvalScores.index(max(pacmanSuccessorsEvalScores))]
     


    def getActionRecursiveHelper(self, gameState, depthCounter):

      numAgents = gameState.getNumAgents()

      #cutoff test
      if((self.depth*numAgents) == depthCounter):
        return self.evaluationFunction(gameState)

      #implement a terminal test
      if(gameState.isWin() ==True or gameState.isLose() == True):
        return self.evaluationFunction(gameState)

      # When it's pacman's turn
      if((depthCounter%numAgents) == self.index): 

        pacmanSuccessors = [] #list of GameStates
        pacmanSuccessorsEvalScores = [] #list of GameStates returned scores

        pacmanLegalActions = gameState.getLegalActions(self.index)

        for action in pacmanLegalActions:
          pacmanSuccessors.append(gameState.generateSuccessor(self.index, action))

        for child in pacmanSuccessors:
          pacmanSuccessorsEvalScores.append(self.getActionRecursiveHelper(child, depthCounter+1))

        return max(pacmanSuccessorsEvalScores)


      #It's a ghost turn
      else: 

        ghostNumber = (depthCounter%numAgents) #which ghost is it?
        ghostSuccessors = [] #list of GameStates
        ghostSuccessorsEvalScores = [] #list of GameStates returned scores

        ghostLegalActions = gameState.getLegalActions(ghostNumber)

        for action in ghostLegalActions:
          ghostSuccessors.append(gameState.generateSuccessor(ghostNumber, action))

        for child in ghostSuccessors:
          ghostSuccessorsEvalScores.append(self.getActionRecursiveHelper(child, depthCounter+1))
      
        return sum(ghostSuccessorsEvalScores)/len(ghostSuccessorsEvalScores)
    
        

def betterEvaluationFunction(currentGameState): 

    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: This evaluation function looks at the current position of pacman,
      the current positions of all the food pellets, the current position of all of the ghosts,
      and the current position of all of the food capsules. The function calculates a food score,
      a capsule score, and the distances to each ghost. The function rewards states where there are
      fewer pellets of food and where there is food closer by. It also rewards states where there are
      fewer food capsules and where food capsules are closer to pacman. Lastly, the function punishes
      states where a ghost is close to Pacman. 
    """
    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    currentGhostStates = currentGameState.getGhostStates()
    currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]
    currentCapsules = currentGameState.getCapsules()


    foodList = currentFood.asList()
    numFood = len(foodList)
    foodDistances = []
    finalScore = 0.0
    foodScore = 0.0
    originalFoodScore = 0.0
    closestFoodScore = 0.0


    ## CREATE A FOOD SCORE
    for food in foodList:    
            foodDistances.append(manhattanDistance(currentPos, food))
   
    # if there's no food left in the game
    if(numFood == 0): 
      # then this state is really good
      return 1000000
     
    else:
      # reward states with less food
      originalFoodScore = 2.5 * (1.0/numFood)
      
      # and reward states that have food that are close by
      closestFoodDistance = min(foodDistances)
      
      # if there's food right next to pacman this is a good state
      if closestFoodDistance == 0:
        closestFoodScore = 200.0

      # otherwise make it so closer food gets a higher score
      else:  
        closestFoodScore = 2.80 * (1.0/closestFoodDistance) 

      # create a final food score
      foodScore = closestFoodScore + originalFoodScore


    ## CREATE A CAPSULE SCORE
    capsuleScore = 0.0
    distanceToCapsules = []
    minCapsuleDistance = None 

    for capsule in currentCapsules:
      distanceToCapsules.append(manhattanDistance(currentPos, capsule))

    if not len(distanceToCapsules) == 0:
      minCapsuleDistance = min(distanceToCapsules)
      # reward being close to ghosts and capsules
      if minCapsuleDistance == 0:
        capsuleScore = 500.0
      else:
        capsuleScore = 2.80 * (1.0/(minCapsuleDistance))#+closestGhostDistance))
    else:
      capsuleScore = 20.0 #20.0
    

    ## FIND DISTANCES TO GHOSTS
    #creates a list of distances to ghosts
    distanceToGhosts = []
    for ghost in currentGhostStates:
      distanceToGhosts.append(manhattanDistance(currentPos, ghost.getPosition()))

    # manhattan distance to the closest ghost
    closestGhostDistance = min(distanceToGhosts)

    
    ## CREATE A FINALSCORE TO RETURN
    # if the ghost is right next to pacman thats bad
    if closestGhostDistance == 0:
      finalScore -= 100.0

    # otherwise scale the distance to the ghost and add in the foodscore and capsulescore
    else:
      finalScore -= 2.0 * (1.0/closestGhostDistance)

      finalScore += foodScore + capsuleScore
    

    return finalScore + scoreEvaluationFunction(currentGameState)

 
# Abbreviation
better = betterEvaluationFunction

