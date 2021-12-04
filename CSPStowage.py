import sys
from state import State
from constraint import *
from defconstraint import ConstraintFunctions


class RunProblem:
    def __init__(self, **arg):
        self.problem = Problem()
        self.variables = []
        self.domain = []
        self.state = State()
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
        self.state.init_map(file_map)

        # Obtain list of containers
        self.state.init_containers(file_container)

        # Add variables and domains
        self.variables = range(len(self.state.containers))  # => [0, 1, 2, 3, 4, 5, 6, ... , n]
        for i in range(len(self.state.layout)):
            for j in range(len(self.state.layout[i])):
                if self.state.layout[i][j] != 'X':
                    cell = (i, j)
                    self.domain.append(cell)  # => [(0,0), (0,1), (0,2), (1,0) ...]

        # self.problem.addVariables(self.variables, self.domain)
        for x in self.variables:
            typeContainer = self.state.containers[x][2]
            if typeContainer == "S":
                self.problem.addVariable(x, [d for d in self.domain if self.state.layout[d[0]][d[1]] == 'N'])

            else:  # typeContainer == "R"
                self.problem.addVariable(x, [d for d in self.domain if self.state.layout[d[0]][d[1]] == 'E'])

    def add_constraints(self):
        c = ConstraintFunctions()

        # Constraint 1: not equal cells / container
        self.problem.addConstraint(AllDifferentConstraint())

        # Constraint 2: There cannot be a container in a cell whose 'below' cells are empty
        self.problem.addConstraint(c.constraintNotFloatingCell(x, self.state.layout, self.variables)
                                   for x in self.variables)

        # Constraint 3:  There cannot be a redistribution of cells in Port 1
        self.problem.addConstraint(
            c.constraintNoRedistribution(x, self.state.layout, self.variables, self.state.containers)
            for x in self.variables if self.state.containers[x][2] == 2)

    def find_solutions(self):

        self.problem.getSolutions()


def readCommand(argv):
    """
    Processes the command used to run stowage from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python stowage.py <options>
    EXAMPLES:   (1) 
    """
    parser = OptionParser(usageStr)

    # -p <path> -m <map> -c <containers>
    parser.add_option('-p', '--path', dest='path', type='text',
                      help=default('the PATH to test files: map and containers'), metavar='PATH', default="./tests")
    parser.add_option('-l', '--layout', dest='layout',
                      help=default('the MAP_FILE from which to load the map layout'),
                      metavar='LAYOUT_FILE')
    parser.add_option('-c', '--container', dest='container',
                      help=default('the CONTAINER_FILE from which to load the list of containers and their types'),
                      metavar='CONTAINERS_FILE')

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    args = dict()

    # Choose a layout map
    args['layout'] = options.path + options.layout
    if args['layout'] is None: raise Exception("The layout " + options.layout + " cannot be found")

    # Choose a container list
    args['container'] = options.path + options.container
    if args['container'] is None: raise Exception("The container list " + options.container + "cannot be found")

    return args


if __name__ == '__main__':
    """
    The main function called when CSPStowage.py is run
    from the command line:

    > python CSPStowage.py <options>

    """
    args = readCommand(sys.argv[1:])  # Get game components based on input
    RunProblem(**args)

    pass
