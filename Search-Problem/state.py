"""
 state.py: contains class of Boat (port_staying, current_stowage),
                            State (Ports, Boat)
"""
import re


class Boat(object):
    def __init__(self, port: int, stowage: list):
        self.port = port
        self.stowage = stowage
        self.layout = stowage

    def _is_valid(self):
        if self._notFloating() and self.port in range(3):
            return True
        return False

    def _notFloating(self):
        # check every container is not floating
        depth = len(self.stowage[0])
        stack = len(self.stowage)

        for s in range(stack):
            stack_str = ' '.join([c if type(c) == str else c[0] for c in self.stowage[s]])
            if re.match("" , stack_str):
                return False

        return True


class State:
    def __init__(self, ports: list, boat: object):
        self.ports = ports  # container = (id, type, port_destination)
        self.boat = boat

    def is_goal(self):
        if self.ports == self.get_Final():
            return True
        return False

    def get_init_goal(self, file_containers, file_layout):
        # TODO: obtain containers for port0 from file
        file_containers.open()
        port0 = []

        initPorts = [port0, [], []]

        # TODO: obtain layout of Boat Stowage from file
        file_layout.open()
        layout0 = []
        initBoat = Boat(0, layout0)

        self.INITIAL_STATE = (initPorts, initBoat)

        # TODO: obtain final distribution of ports
        port1 = []
        port2 = []

        finalPorts = [[], port1, port2]

        # obtain final layout of Boat
        finalBoat = Boat(2, layout0)

        self.FINAL_STATE = (finalPorts, finalBoat)

    def get_Init(self):
        return self.INITIAL_STATE

    def get_Final(self):
        return self.FINAL_STATE
