class Action:
    """
    Action:  Abstract Class, no implementation
    """

    def __init__(self, cost, *args):
        self.cost = cost

    def applyAction(self, state):
        """Return New State"""
        pass


class Sail(Action):
    def __init__(self, cost, port_init, port_final):
        self.cost = cost
        self.port_init = port_init
        self.port_final = port_final
        super().__init__(self.cost, self.port_init, self.port_final)

    def applyAction(self, state):
        # TODO: make changes in state(port, boat) with init data
        pass

    def __str__(self):
        return "Sail ( Origin: {0}, Destination: {1})".format(self.port_init, self.port_final)


class Load(Action):
    def __init__(self, cost, port, c, cell):
        self.cost = cost
        self.port = port
        self.container = c
        self.cell = cell
        super().__init__(self.cost, self.port, self.container, self.cell)

    def applyAction(self, state):
        #TODO: make changes in state(port, boat) with init data
        pass

    def __str__(self):
        return "Load (Port: {0}, Container: {1}, Cell: {2})".format(self.port, self.container, self.cell)


class Unload(Action):
    def __init__(self, cost, port, c, cell):
        self.cost = cost
        self.port = port
        self.container = c
        self.cell = cell
        super().__init__(self.cost, self.port, self.container, self.cell)

    def applyAction(self, state):
        # TODO: make changes in state(port, boat) with init data
        pass

    def __str__(self):
        return "Unload (Port: {0}, Container: {1}, Cell: {2})".format(self.port, self.container, self.cell)

