"""
 state.py: contains class of Boat (port_staying, current_stowage),
                            State (Ports, Boat)
"""
import re
from file_constants import Constant

CRED = '\033[91m'
CEND = '\033[0m'


class Boat(object):
    def __init__(self, port: int, stowage: list):
        self.port = port
        self.stowage = stowage

    def _notFloating(self):
        # check every container is not floating
        stack = len(self.stowage)

        for s in range(stack):
            stack_str = ''.join([c if type(c) == str else c[0] for c in self.stowage[s]])
            regex = r'(N|E)*\d*X+'
            if not re.fullmatch(regex , stack_str):
                return False
        return True

    def get_container_stowage(self):
        containers = 0
        for stack in self.stowage:
            for cell in stack:
                if cell not in ('N', 'E', 'X'):
                    containers += 1
        return containers


class State:

    def __init__(self, ports: list, boat: object):
        self.ports = ports  # container = (id, type, port_destination)
        self.boat = boat

    def get_all_containers(self):
        return self.port0

    def get_layout(self):
        return self.layout0

    def is_goal(self):
        if self.ports == self.get_Final():
            return True
        return False

    def get_init_goal(self, file_containers, file_layout):

        #obtain containers for port0 from file

        port0 = Constant.init_containers(file_containers)

        initPorts = [port0, [], []]

        #obtain layout of Boat Stowage from file

        layout0 = Constant.init_map(file_layout)
        initBoat = Boat(0, layout0)

        self.INITIAL_STATE = State(initPorts, initBoat)

        #obtain final distribution of ports
        port1 = []
        port2 = []
        for c in port0:
            if c[2] == '1':
                port1.append(c)
            elif c[2] == '2':
                port2.append(c)

        finalPorts = [[], port1, port2]

        #obtain final layout of Boat
        finalBoat = Boat(1, layout0)
        finalBoat2 = Boat(2, layout0)
        self.FINAL_STATE = [State(finalPorts, finalBoat), State(finalPorts, finalBoat2)]

        self.port0 = port0
        self.layout0 = layout0

    def get_Init(self):
        return self.INITIAL_STATE

    def get_Final(self):
        return self.FINAL_STATE