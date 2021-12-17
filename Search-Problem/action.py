class Action:
    """
    Action:  Abstract Class, no implementation
    """

    def isLegal(self, state):
        pass

    def applyAction(self, state):
        """Return New State"""
        pass

    def costAction(self):
        pass


class Sail(Action):
    def __init__(self, port_init: int, port_final: int):
        self.port_init = port_init
        self.port_final = port_final
        super().__init__(self.port_init, self.port_final)

    def applyAction(self, state):
        #make changes in boat port position
        state.boat.port = self.port_final
        return state

    def isLegal(self, state):
        #check preconditions: boat in port_origin
        return state.boat.port == self.port_init

    def costAction(self):
        return 3500

    def __str__(self):
        return "Sail ( Origin: {0}, Destination: {1})".format(self.port_init, self.port_final)


class Load(Action):
    def __init__(self, port: int, c: tuple, cell: tuple):
        self.port = port
        self.container = c
        self.cell = cell
        super().__init__(self.port, self.container, self.cell)

    def applyAction(self, state):
        #make changes in state(port, boat) with init data: port-cont, stowage+cont
        state.boat.stowage[self.cell[0]][self.cell[1]] = self.container
        state.port[self.port].remove(self.container)

        return state

    def isLegal(self, state):
        #check preconditions: Cell is Empty, State.Boat.notfloating, boat_port, special_cell, cont_port

        #proving that the cell we want to load is not floating
        if not state.boat._notFloating():
            return False

        #Proving that we can insert the container in the Standard or Refrigerated
        if not state.boat.stowage[self.cell[0]][self.cell[1]] in ('N', 'E'):
            return False

        #Check that the boat is in the port
        if self.port != state.boat.port:
            return False

        #Checking that if the container is energy needs to go into the refrigerated
        if self.container[1] == 'E' and state.boat.stowage[self.cell[0]][self.cell[1]] != 'E':
            return False

        #Checking that the container we want to load is in the port
        if self.container not in state.ports[self.port]:
            return False

        return True

    def costAction(self):
        return 10 + self.cell[1]

    def __str__(self):
        return "Load (Port: {0}, Container: {1}, Cell: {2})".format(self.port, self.container, self.cell)


class Unload(Action):
    def __init__(self, port: int, c: tuple, cell: tuple):
        self.port = port
        self.container = c
        self.cell = cell
        super().__init__(self.port, self.container, self.cell)

    def applyAction(self, state):
        # make changes in state(port, boat) with init data: stowage-cont, port + cont
        state.port[self.port].append(self.container)
        state.boat.stowage[self.cell[0]][self.cell[1]] = state.boat.layout[self.cell[0]][self.cell[1]]
        return state

    def isLegal(self, state):
        #check preconditions: cell_top_empty, boat_port, Exists_cont_cell
        depth = self.cell[1]
        stack = self.cell[0]

        #check that there is no container over the one to unload
        for k in range(depth):
            if state.boat.stowage[stack][k] not in ('N', 'E'):
                return False

        #Check that the boat is in the port
        if self.port != state.boat.port:
            return False

        #Check that the Container to extract is in the cell specified
        if state.boat.stowage[stack][depth] != self.container:
            return False

        return True

    def costAction(self):
        return 15 + 2*self.cell[1]

    def __str__(self):
        return "Unload (Port: {0}, Container: {1}, Cell: {2})".format(self.port, self.container, self.cell)

