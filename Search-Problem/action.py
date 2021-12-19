import copy


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

    def applyAction(self, state):
        # make changes in boat port position
        new_state = copy.deepcopy(state)
        new_state.boat.port = self.port_final
        return new_state

    def isLegal(self, state):
        # check preconditions:

        # Boat in port_origin
        if state.boat.port != self.port_init:
            return False

        # ---------- Specific Precondition to reduce Nodes Generated -----------------

        #Fill all space in boat stowage
        if state.boat.port == 0 and state.boat.get_space_stowage() >= len(state.ports[0]) > 0 :
            return False

        # In Port 1: Do all Unload/Load redistributions
        if state.boat.port == 1:
            # Verify that there are no containers to port 1 in boat,
            if '1' in [cont[2] for cont in state.boat.get_container_stowage()]:
                return False
            # or no container to port 2 in port 1
            if '2' in [cont[2] for cont in state.ports[1]]:
                return False

        return True

    def costAction(self):
        return 3500

    def __str__(self):
        return "Sail (Origin: {0}, Destination: {1})".format(self.port_init, self.port_final)


class Load(Action):
    def __init__(self, port: int, c: tuple, cell: tuple):
        self.port = port
        self.container = c
        self.cell = cell

    def applyAction(self, state):
        # make changes in state(port, boat) with init data: port-cont, stowage+

        new_state = copy.deepcopy(state)
        new_state.boat.stowage[self.cell[0]][self.cell[1]] = self.container
        new_state.ports[self.port].remove(self.container)

        return new_state

    def isLegal(self, state):
        # check preconditions: Cell is Empty, State.Boat.notfloating, boat_port, special_cell, cont_port

        # proving that the cell we want to load is not floating
        if not state.boat._notFloating():
            return False

        # Proving that we can insert the container in the Standard or Refrigerated
        if state.boat.stowage[self.cell[0]][self.cell[1]] not in ('N', 'E'):
            return False

        # Check that the boat is in the port
        if self.port != state.boat.port:
            return False

        # Checking that if the container is energy needs to go into the refrigerated
        if self.container[1] == 'R' and state.boat.stowage[self.cell[0]][self.cell[1]] != 'E':
            return False

        # Checking that the container we want to load is in the port
        if self.container not in state.ports[self.port]:
            return False

        # ----------Reducing Nodes -------------
        # Check that the port is not 2
        if self.port == 2:
            return False

        # Check that the container is not in its destinations
        if str(self.port) == self.container[2]:
            return False

        return True

    def costAction(self):
        return 10 + self.cell[1]

    def __str__(self):
        return "Load (Port: {0}, Container: {1}, Cell: {2})".format(self.port, self.container[0], self.cell)


class Unload(Action):
    def __init__(self, port: int, c: tuple, cell: tuple):
        self.port = port
        self.container = c
        self.cell = cell

    def applyAction(self, state):
        # make changes in state(port, boat) with init data: stowage-cont, port + cont
        new_state = copy.deepcopy(state)
        new_state.ports[self.port].append(self.container)
        layout = state.get_layout()
        new_state.boat.stowage[self.cell[0]][self.cell[1]] = layout[self.cell[0]][self.cell[1]]
        return new_state

    def isLegal(self, state):
        # check preconditions: cell_top_empty, boat_port, Exists_cont_cell
        depth = self.cell[1]
        stack = self.cell[0]

        # check that there is no container over the one to unload
        for k in range(depth):
            if k != 0 and state.boat.stowage[stack][k] not in ('N', 'E'):
                return False

        # Check that the boat is in the port
        if self.port != state.boat.port:
            return False

        # Check that the Container to extract is in the cell specified
        if state.boat.stowage[stack][depth] != self.container:
            return False

        # -------------- Reducing nodes ---------------

        # Check that the port is not 0
        if state.boat.port == 0:
            return False

        #Check all containers go to Port 2
        if state.boat.port == 1 and '1' not in [cont[2] for cont in state.boat.get_container_stowage()]:
            return False

        return True

    def costAction(self):
        return 15 + 2 * self.cell[1]

    def __str__(self):
        return "Unload (Port: {0}, Container: {1}, Cell: {2})".format(self.port, self.container[0], self.cell)
