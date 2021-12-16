
class State:
    def __init__(self, ports: object, boat: object):
        self.ports = ports
        self.boat = boat

    def is_goal(self):
        if self.ports == self.get_Final():
            return True
        return False

    def is_valid(self):
        self.boat._is_valid()

    def get_Init_Goal(self, file_containers, file_layout):

        #TODO: obtain containers for port0 from file
        file_containers.open()
        port0 = []
        initPorts = Ports(port0, [], [])

        #TODO: obtain layout of Boat Stowage from file
        file_layout.open()
        layout0 = []
        initBoat = Boat(0, layout0)

        self.INITIAL_STATE = (initPorts, initBoat)

        #TODO: obtain final distribution of ports
        port1 = []
        port2 = []
        finalPorts = Ports([], port1, port2)

        #obtain final layout of Boat
        finalBoat = Boat(2, layout0)

        self.FINAL_STATE = (finalPorts, finalBoat)

    def get_Init(self):
        return self.INITIAL_STATE

    def get_Final(self):
        return self.FINAL_STATE


class Ports (object):
    def __init__(self, port0=[], port1=[], port2=[]):
        self.port0 = port0
        self.port1 = port1
        self.port2 = port2


class Boat(object):
    def __init__(self, port, layout):
        self.port = port
        self.layout = layout

    def _is_valid(self):
        if _notFloating(self.layout) and self.port in range(3):
            return True
        return False

    def _notFloating(self):
        #TODO: check every container is not floating
        return True
