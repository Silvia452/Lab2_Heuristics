import sys
import os
from search import aStarSearch
from StowageProblem import StowageProblem
import time


def main(path, layout, container, heur):

    usageStr = """
    USAGE:      python
    EXAMPLES:   (1) python 
    """
    file_map = os.getcwd() + r'/' + path + r'/' + layout
    if not os.path.isfile(file_map): raise Exception("The layout " + file_map + " cannot be found")

    # Choose a container list
    file_containers = os.getcwd() + r'/' + path + r'/' + container
    if not os.path.isfile(file_containers): raise Exception("The container list " + file_containers + "cannot be found")


    #Start running time
    starttime = time.time()
    # Make new Problem data
    problem = StowageProblem(file_containers, file_map)
    # Obtain heuristic method
    heuristic = getattr(StowageProblem, heur)
    # Find Solution Path
    actions = lambda prob : aStarSearch(problem, heuristic=heuristic)
    #Obtain cost from actions
    print(actions)
    totalCost = problem.getCostOfActions(actions(problem))
    print('Solution found with total cost of %d in %.5f seconds' % (totalCost, time.time() - starttime))


if __name__ == '__main__':
    """
    The main function called when CSPStowage.py is run
    from the command line:

    > python main.py <options>

    """
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

