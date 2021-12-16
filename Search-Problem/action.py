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
        # TODO: make changes in state(port, boat) with init data
        #state.boat.port = self.port_final
        pass

    def isLegal(self, state):
        #TODO: check preconditions: boat_port
        pass

    def costAction(self):
        #TODO
        pass

    def __str__(self):
        return "Sail ( Origin: {0}, Destination: {1})".format(self.port_init, self.port_final)


class Load(Action):
    def __init__(self, port: int, c: int, cell: tuple):
        self.port = port
        self.container = c
        self.cell = cell
        super().__init__(self.port, self.container, self.cell)

    def applyAction(self, state):
        #TODO: make changes in state(port, boat) with init data: port-cont, stowage+cont
        state.boat.stowage[self.cell[0]][self.cell[1]] = self.container
        state.port[self.port].remove(self.container)
        #continue
        pass

    def isLegal(self, state):
        #TODO: check preconditions: Cell is Empty, State.Boat.notfloating, boat_port, special_cell, cont_port
        pass

    def costAction(self):
        return 10 + self.cell[1]

    def __str__(self):
        return "Load (Port: {0}, Container: {1}, Cell: {2})".format(self.port, self.container, self.cell)


class Unload(Action):
    def __init__(self, port: int, c: int, cell: tuple):
        self.port = port
        self.container = c
        self.cell = cell
        super().__init__(self.port, self.container, self.cell)

    def applyAction(self, state):
        # TODO: make changes in state(port, boat) with init data: stowage-cont, port + cont
        pass

    def isLegal(self, state):
        #TODO: check preconditions: cell_top_empty, boat_port, Exists_cont_cell
        pass

    def costAction(self):
        #TODO
        pass

    def __str__(self):
        return "Unload (Port: {0}, Container: {1}, Cell: {2})".format(self.port, self.container, self.cell)

