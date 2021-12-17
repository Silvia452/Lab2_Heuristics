"""
 state.py: contains class of Boat (port_staying, current_stowage),
                            State (Ports, Boat)
"""
import re
import sys

CRED = '\033[91m'
CEND = '\033[0m'

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
        stack = len(self.stowage)

        for s in range(stack):
            stack_str = ''.join([c if type(c) == str else c[0] for c in self.stowage[s]])
            regex = r'(N|E)*\d*X+'
            if not re.fullmatch(regex , stack_str):
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


        #obtain containers for port0 from file

        port0 = self.init_containers(file_containers)
        initPorts = [port0, [], []]

        #obtain layout of Boat Stowage from file

        layout0 = self.init_map(file_layout)
        initBoat = Boat(0, layout0)

        self.INITIAL_STATE = (initPorts, initBoat)

        #obtain final distribution of ports
        port1 = []
        port2 = []
        for c in port0:
            if c[2] == 1:
                port1.append(c)
            elif c[2] == 2:
                port2.append(c)

        finalPorts = [[], port1, port2]

        #obtain final layout of Boat
        finalBoat = Boat(2, layout0)

        self.FINAL_STATE = (finalPorts, finalBoat)

    def get_Init(self):
        return self.INITIAL_STATE

    def get_Final(self):
        return self.FINAL_STATE

    def init_map(self, file):
            """From file map: (stack, depth)
                        N N N N     (0,0) (1,0) (2,0) (3,0)
                        N N N N     (0,1) (1,1) (1,2) (3,1)
                        E N N E     (0,2) (1,2) (2,2) (3,2)
                        X E E X           (1,3) (2,3)
                        X X X X
            """
            layout = []
            with open(file) as handle:
                raw_lines = handle.read().split('\n')

            for n in range(len(raw_lines[0].split())):
                layout.append([])

            for line in raw_lines:
                regex = r"((N|E|X)\s)*(N|E|X){1}(\n)*"

                line_list = line.split()  # => [N,N,N,N]

                for n in range(len(line_list)):
                    if re.match(regex, line_list[n]) is None:
                        print(line_list[n])
                        print(CRED + 'error parsing test file: %s' % file + CEND)
                        sys.exit(1)
                    else:
                        layout[n].append(line_list[n])
            """Read output:
                    => layout =  [  ['N', 'N', 'E', 'X', 'X'], 
                                    ['N', 'N', 'N', 'E', 'X'],
                                    ['N', 'N', 'N', 'E', 'X'],
                                    ['N', 'N', 'E', 'X', 'X']
                                ]

            """

            return layout

        def init_containers(self, file):
            """
            From file containers:
                1 S 1
                2 S 1
                3 S 1
                4 R 2
                5 R 2

            Read output:
                => containers = [(1,S,1), (2,S,1), (3,S,1), (4,R,2), (5,R,2)]

                containers[i] = "i"
            """
            containers = []

            with open(file) as handle:
                raw_lines = handle.read().split('\n')

            for line in raw_lines:
                regex = r"\d+ (S|R) (1|2)\n?"

                if not re.match(regex, line):
                    print(CRED + 'error parsing test file: %s' % file + CEND)
                    sys.exit(1)
                else:
                    containers.append(tuple(line.split()))

            return containers

