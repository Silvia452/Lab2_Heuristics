"""
search.py: generic search algorithms
"""
from builtins import object
from util import PriorityQueueWithFunction

class SearchProblem(object):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    """
    def __init__(self, state, goal):
        self.init = state
        self.goal = goal

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        return self.init

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        return state == self.goal

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a
        list of triples,[ (successor, action, stepCost), (succ2, acc2, cost2), ... ]
        where 'successor' is a successor to the current state,
         'action' is a legal action required to get there,
         and 'stepCost' is the incremental cost of expanding to that successor.
        """
        pass

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        pass

    def getLegalActions(self, state):
        """
                 state: Search state

                For a given state, this should return a list of legal actions to
                possibly implement.
                """
        pass

def generalGraphSearch(problem, structure):
    # Push the root node/start into the data structure in this format: [(state, action taken, cost)]
    # The list pushed into the structure for the second node will look something like this:
    # [(root_state, "No action", 0), (new_state, Action.__str__, Action.cost]
    structure.push([(problem.getStartState(), "No action", 0)])

    # Initialise the list of visited nodes to an empty list
    visited = []
    #cost=0
    #expanded_nodes = 0

    # While the structure is not empty, i.e. there are still elements to be searched,
    while not structure.isEmpty():
        # get the path returned by the data structure's .pop() method
        path = structure.pop()

        # The current state is the first element in the last tuple of the path
        curr_state = path[-1][0]

        # if the current state is the goal state,
        if problem.isGoalState(curr_state):
            # return the actions to the goal state
            # which is the second element for each tuple in the path, ignoring the first "Stop"
            return [x[1] for x in path][1:]

        if curr_state not in visited:
            # mark the current state as visited by appending to the visited list
            visited.append(curr_state)

            #expanded_nodes+=1
            #successor states
            for successor in problem.getSuccessors(curr_state):

                if successor[0] not in visited:
                    # Copy the parent's path
                    successorPath = path[:]
                    # Set the path of the successor node to the parent's path + the successor node
                    successorPath.append(successor)
                    # Push the successor's path into the structure
                    structure.push(successorPath)
    # If search fails, return False
    return False

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    # The cost for a* seach is f(x) = g(x) + h(x)
    # The heuristic is h(x), heuristic(state, problem),
    # where state = path[-1][0], which is the first element in the last tuple of the path
    f = lambda path: problem.getCostOfActions([x[1] for x in path][1:]) + heuristic(path[-1][0], problem)
    h = lambda path: heuristic(path[-1][0], problem)

    # Construct an empty priority queue that sorts using f(x) and breaks ties by h(x)
    pq = PriorityQueueWithFunction((f, h))

    # A* is general graph search with the PriorityQueue sorting by the f(x) as the data structure
    return generalGraphSearch(problem, pq)

