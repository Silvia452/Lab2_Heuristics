#!/bin/bash
import os
import sys
from constraint import *
from file_constants import Constant


class RunProblem:
    def __init__(self, **arg):
        self.problem = Problem()
        self.variables = []
        self.domain = []
        self.init_state(arg['layout'], arg['container'])
        self.add_constraints()

    def init_state(self, file_map, file_container):
        """
        - The variables will be our containers c : [0, 1, 2, 3, 4, 5, 6, ... , n]
        - Domains will be our cells: [(0,0), (0,1), (0,2), (1,0) ...]

        (i,j) : map[stack][depth]      => (0,0) = N; (0,2)=E; (0,3)=X
        var c : container[c]
        """

        # Obtain list of cells (layout map)
        self.layout = Constant.init_map(file_map)

        # Obtain list of containers
        self.containers = Constant.init_containers(file_container)

        # Add variables and domains
        self.variables = range(len(self.containers))  # => [0, 1, 2, 3, 4, 5, 6, ... , n]

        # Domain list without X cells (floor)
        for i in range(len(self.layout)):
            for j in range(len(self.layout[i])):
                if self.layout[i][j] != 'X':
                    cell = (i, j)
                    self.domain.append(cell)  # => [(0,0), (0,1), (0,2), (1,0) ...]

        # self.problem.addVariables(self.variables, self.domain)
        for x in self.variables:
            typeContainer = self.containers[x][1]
            # Add domain to standard containers in normal cells
            if typeContainer == "S":
                self.problem.addVariable(x, [d for d in self.domain])

            # Add domain to refrigerated containers in normal cells
            else:  # typeContainer == "R":
                self.problem.addVariable(x, [d for d in self.domain if self.layout[d[0]][d[1]] == 'E'])

    def add_constraints(self):
        # Constraint 1: not equal cells / container
        self.problem.addConstraint(AllDifferentConstraint(), variables=self.variables)

        # Constraint 2: There cannot be a container in a cell whose 'below' cells are empty
        self.problem.addConstraint(self.constraintNotFloatingCell, variables=self.variables)

        # Constraint 3:  There cannot be a redistribution of cells in Port 1
        for x in self.variables:
            for y in self.variables:
                if self.containers[x][2] == "2" and self.containers[y][2] == "1":
                    self.problem.addConstraint(self.constraintNoRedistribution, variables=[x, y])

        self.find_solution()

    def find_solution(self):
        solutions = self.problem.getSolutions()
        # and show them on the standard output
        print(" #Number of solutions: {0}".format(len(solutions)))
        for i_sol in solutions:
            print(i_sol)
        return solutions

    def constraintNotFloatingCell(self, *container_domain):
        """Constraint: There cannot be a container in a cell whose 'below' cells are empty
                    To assign to the position x =  (i,j), container c : for all k>j
                           (i, k) != empty OR (i,k) == 'X' """

        for cell in container_domain:
            cell_bellow = (cell[0], cell[1] + 1)
            if cell_bellow not in container_domain and self.layout[cell_bellow[0]][cell_bellow[1]] != 'X':
                return False
        return True

    def constraintNoRedistribution(self, container_port_2: tuple, container_port_1: tuple):
        """ - Constraint: There cannot be a redistribution of cells in Port 1:
                                    There cannot be a container 'Port2' over container 'Port1'

                        ***        You cannot assign container c where container[c] == (-, 2) to position (i,j) :
                                    if any (i,k) = c' and container[c'] = (c', -, 1)  for all k>j """

        # see if they are in the same stack
        if container_port_1[0] == container_port_2[0]:
            # see if container to port 1 is above
            if container_port_1[1] < container_port_2[1]:
                return True
            return False
        return True


def main(path, layout, container):

    usageStr = """
    USAGE:      python python CSPStowage.py -p <path> -l <map> -c <containers>
    EXAMPLES:   (1) python python CSPStowage.py -p CSP-tests -l map1 -c contenedores1
    """
    map = os.getcwd() + r'/' + path + r'/' + layout
    if map is None: raise Exception("The layout " + layout + " cannot be found")

    # Choose a container list
    cont = os.getcwd() + r'/' + path + r'/' + container
    if cont is None: raise Exception("The container list " + container + "cannot be found")

    solution = RunProblem(layout=map, container=cont)

    #write file solution
    file_sol = os.getcwd() + r'/' + path + r'/' + layout + '-' + container + '.output'
    fd_sol = open(file_sol, 'w')

    fd_sol.write(" #Number of solutions: " + str(len(solution)))
    for s in solution:
        fd_sol.write(str(s))

    fd_sol.close()


if __name__ == '__main__':
    """
    The main function called when CSPStowage.py is run
    from the command line:

    > python CSPStowage.py <options>

    """
    main(sys.argv[1], sys.argv[2], sys.argv[3])
