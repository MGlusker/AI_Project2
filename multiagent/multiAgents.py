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

        pacmanLegalActions = gameState.getLegalActions(self.index)

        for action in pacmanLegalActions:
          pacmanSuccessors.append(gameState.generateSuccessor(self.index, action))
        
        for child in pacmanSuccessors:
          pacmanSuccessorsEvalScores.append(self.getActionRecursiveHelper(child, 1))

        return pacmanLegalActions[pacmanSuccessorsEvalScores.index(max(pacmanSuccessorsEvalScores))]
     


    def maxRecursiveHelper(self, gameState, depthCounter, alpha, beta):

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


      def minRecursiveHelper(self, gameState, depthCounter, alpha, beta)

        numAgents = gameState.getNumAgents()

        #cutoff test
        if((self.depth*numAgents) == depthCounter):
          return self.evaluationFunction(gameState)

        #implement a terminal test
        if(gameState.isWin() ==True or gameState.isLose() == True):
          return self.evaluationFunction(gameState)

        ghostNumber = (depthCounter%numAgents) #which ghost is it?
        ghostSuccessors = [] #list of GameStates
        ghostSuccessorsEvalScores = [] #list of GameStates returned scores

        ghostLegalActions = gameState.getLegalActions(ghostNumber)

        for action in ghostLegalActions:
          ghostSuccessors.append(gameState.generateSuccessor(ghostNumber, action))

        for child in ghostSuccessors:
          ghostSuccessorsEvalScores.append(self.getActionRecursiveHelper(child, depthCounter+1))
      
        return min(ghostSuccessorsEvalScores)
        """
        
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

