from search.search import aStarSearch
from StowageProblem import StowageProblem
import time


def registerSearch(file1, file2):
    starttime = time.time()
    problem = StowageProblem(file1, file2)  # Make new Problem data
    actions = lambda x: aStarSearch(problem, heuristic=function2)  # Find Path
    totalCost = problem.getCostOfActions(actions)
    print('Solution found with total cost of %d in %.5f seconds' % (totalCost, time.time() - starttime))

file1 = "./Search-Problem/Search-tests/map1"
file2 = "./Search-Problem/Search-tests/container1"

registerSearch(file1, file2)
