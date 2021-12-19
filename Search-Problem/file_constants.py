import re
import sys

CRED = '\033[91m'
CEND = '\033[0m'


class Constant:

    @staticmethod
    def init_map(file):
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

        stack = 0
        for line in raw_lines:
            regex = r"((N|E|X)\s)*(N|E|X){1}(\n)*"

            line_list = line.split()  # => [N,N,N,N]

            if stack == 0:
                stack = len(line_list)
            else:
                if stack != len(line_list):
                    print(print(CRED + 'error parsing test file: %s' % file + CEND))
                    sys.exit(1)

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
        _LIST_LAYOUT_ = layout
        return layout

    @staticmethod
    def init_containers(file):
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
