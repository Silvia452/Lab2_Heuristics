import re
import sys

CRED = '\033[91m'
CEND = '\033[0m'


class State:
    def __init__(self):
        self.layout = []
        self.containers = []

    def init_map(self, file):
        """From file map: (stack, depth)
                    N N N N     (0,0) (1,0) (2,0) (3,0)
                    N N N N     (0,1) (1,1) (2,1) (3,1)
                    E N N E     (0,2) (1,2) (2,2) (3,2)
                    X E E X     (0,3) (1,3) (2,3) (3,3)
                    X X X X
        """

        with open(file) as handle:
            raw_lines = handle.read().split('\n')

        for line in raw_lines:
            regex = r"((N|E|X)\s)*(N|E|X){1}(\n)*"
            self.layout.append(line.split())
            """if re.match(line, regex) is None:
                print(line)
                print(CRED + 'error parsing test file: %s' % file + CEND)
                sys.exit(1)
            else:
                self.layout.append(line.split())"""

        """Read output:
                => layout =  [ [N,N,N,N], [N,N,N,N], [E,N,N,E], [X,E,E,X], [X,X,X,X]]
        """

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

        with open(file) as handle:
            raw_lines = handle.read().split('\n')

        for line in raw_lines:
            regex = r"\d+ (S|R) (1|2)\n?"
            self.containers.append(tuple(line.split()))
            """if not re.match(line, regex):
                print(CRED + 'error parsing test file: %s' % file + CEND)
                sys.exit(1)
            else:
                self.containers.append(tuple(line.split()))
"""