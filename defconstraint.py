class ConstraintFunctions:
    def __init__(self):
        pass

    """    @staticmethod
    def constraintsNormalCell(x, layout, y, containers):
        #Constraint: In normal cell only standard containers
         #           x:cell (i,j)     y: container y
          #          layout: map      containers: list of containers
                   
        if layout[x[0], x[1]] == 'N' and containers[y][1] == 'S':
            layout[x[0]][x[1]] = y
            return True
        return False

    @staticmethod
    def constraintRefrigeratedCell(x, layout, y, containers):
       # Contraint: In energy cell only standard refrigerated
        if layout[x[0], x[1]] == 'E' and containers[y][1] == 'R':
            layout[x[0]][x[1]] = y
            return True
        return False"""

    @staticmethod
    def constraintNotFloatingCell(cell, layout, variables):
        """Constraint: There cannot be a container in a cell whose 'below' cells are empty
                 k is the cells with more depth (below) j of (i,j) in stack (column) i

                        To assign to the position x =  (i,j), container c : for all k>j
                           (i, k) != empty OR (i,k) == 'X' """

        # cell = (i, j) : where container c should be allocated
        # variables is the list with their values assigned: [(m,n), (m,n), ...]
        # layout is the map: [ [N, N, N, N], [E, E, E, E], ...]

        for k in range(cell[1] + 1, len(layout)):  # iterate through depth
            if layout[cell[0]][k] is "X":
                return True
            else:
                for x in variables:
                    if x[0] == cell[0] and x[1] == k:
                        return True
                return False

    @staticmethod
    def constraintNoRedistribution(cell, layout, variables, container):
        """ - Constraint: There cannot be a redistribution of cells in Port 1:
                            There cannot be a container 'Port2' over container 'Port1'

                ***        You cannot assign container c where container[c] == (-, 2) to position (i,j) :
                            if any (i,k) = c' and container[c'] = (c', -, 1)  for all k>j """

        for k in range(cell[1] + 1, len(layout)):  # iterate through depth
            if layout[cell[0]][k] is "X":
                return True
            else:
                for x in variables:
                    if x[0] == cell[0] and x[1] == k and container[x][2] == 1:
                        return False
                return True
