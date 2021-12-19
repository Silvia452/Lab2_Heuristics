import sys
import os
from search import aStarSearch
from StowageProblem import StowageProblem
import time


def main(path, layout, container, heur):
    #Choose the layout file
    file_map = os.getcwd() + r'/' + path + r'/' + layout
    if not os.path.isfile(file_map): raise Exception("The layout " + file_map + " cannot be found")

    # Choose the container list
    file_containers = os.getcwd() + r'/' + path + r'/' + container
    if not os.path.isfile(file_containers): raise Exception("The container list " + file_containers + "cannot be found")

    # Write the solution file
    file_solution = os.getcwd() + r'/' + path + r'/' + layout + '-' + container + '-' + heur + '.output'
    fd_sol = open(file_solution, 'a')

    #Write the statistic file
    file_stat = os.getcwd() + r'/' + path + r'/' + layout + '-' + container + '-' + heur + '.stat'
    fd_stat = open(file_stat, 'w')

    #Start running time
    starttime = time.time()

    # Make new Problem data
    problem = StowageProblem(file_containers, file_map)

    # Obtain heuristic method
    heuristic = getattr(StowageProblem, heur)

    # Find Solution Path
    actions = lambda prob : aStarSearch(problem, heuristic=heuristic)
    solution, nodes = actions(problem)
    #Obtain Solution Statistics
    totalCost = problem.getCostOfActions(solution)
    init_sol = 'Solution Path:\n'
    fd_sol.write(init_sol)

    i = 0
    for step in solution:
        line = '{}.\t{}\n'.format(i, step)
        fd_sol.write(line)
        i +=1

    str_stat = 'Expanded nodes: %d\nOverall cost: %d \nPlan length: %d\nOverall time: %.5f seconds' % (nodes, totalCost,len(solution) ,time.time() - starttime)

    fd_stat.write(str_stat)
    fd_sol.close()
    fd_stat.close()


if __name__ == '__main__':
    """
    The main function called when CSPStowage.py is run
    from the command line:

    > python main.py <options>

    """
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

