import re

from state import State
from action import Load, Sail, Unload
from search import SearchProblem


class StowageProblem(SearchProblem):
    def __init__(self, file_containers, file_layout):
        state = State([], None)
        state.get_init_goal(file_containers, file_layout)
        initial_state = state.get_Init()
        goal_state = state.get_Final()
        super().__init__(initial_state, goal_state)
        self.containers = state.get_all_containers()
        self.layout = state.get_layout()

    def getLegalActions(self, state):
        all_actions = self.get_all_actions()
        return self.get_valid_actions(state, all_actions)

    def get_all_actions(self):
        """action = Load(cost, port, c, cell) /
                    Sail(cost, port_init, port_final)
                    Unload(cost, port, c, cell)"""

        # sail
        all_act = [Sail(0, 1), Sail(1, 2)]
        # load/unload from port 0/1/2
        for p in range(2):
            # obtain tuples of containers
            for cont in self.containers:
                # obtain each cell of boat stowage
                for cell_x in range(len(self.layout)):
                    for cell_y in range(len(self.layout[cell_x])):
                        all_act.append(Load(p, cont, (cell_x, cell_y)))
                        all_act.append(Unload(p, cont, (cell_x, cell_y)))
        return all_act

    def get_valid_actions(self, state, all_action):
        """
        get possible actions by checking preconditions
        :param all_action: list of all possible actions (not validated)
        :param state: current state (port, boat)
        :return: list of objects Actions: Load, Sail, Unload, with the
        necessary paramenters which can be applied from state
        """
        valid_actions = []

        for action in all_action:
            if action.isLegal(state):
                valid_actions.append(action)

        return valid_actions

    def getSuccessors(self, state):
        succesors = []

        for action in self.getLegalActions(state):
            newstate = action.applyAction(state)
            str_action = action.__str__()
            stepCost = action.costAction()
            succesors.append((newstate, str_action, stepCost))
        # print('\nFor State: P:{}, B:{}\t{}'.format(state[0], state[1].port, state[1].stowage))
        return succesors

    def getCostOfActions(self, actions):
        # 'Sail (Origin: 0, Destination: 1)'
        # 'Load (Port: 0, Container: 0, Cell: (0,0))'
        totalCost = []
        sail = r'Sail: \(Origin: (\d+), Destination: (\d+)\)'
        load = r'Load: \(Port: (\d+), Container: (\d+), Cell: \((\d+),(\d+)\)\)'
        unload = r'Unload: \(Port: (\d+), Container: (\d+), Cell: \((\d+),(\d+)\)\)'
        for action in actions:
            args = re.findall(r'\d+', action)
            if re.match('Sail', action):
                totalCost.append(Sail(int(args[0]), int(args[1])).costAction())
            else:
                container = self.containers[int(args[1])]
                cell = (int(args[2]), int(args[3]))
                if re.match('Load', action):
                    totalCost.append(Load(args[0], container, cell).costAction())
                elif re.match('Unload', action):
                    totalCost.append(Unload(args[0], container, cell).costAction())
        return sum(totalCost)

    def isGoalState(self, state):
        # print('\nFor State: P:{}, B:{}\t{}'.format(state[0], state[1].port, state[1].stowage))
        # print('Goal State: P:{}, B:{}\t{}'.format(self.goal[0], self.goal[1].port, self.goal[1].stowage))
        for goal in self.goal:
            if goal.ports == state.ports and goal.boat.port == state.boat.port \
                    and goal.boat.stowage == state.boat.stowage:
                return True
        return False

    def getEstimation2Boats(self, state):
        """
        Sail 2 boats simultaneously:
            Boat A : From Port0 --> Port1
            Boat B : From Port1 --> Port2

        Uniform Cost for all Actions
        :param state: State obj
        :return: int estimation cost to reach Goal State
        """
        loadCost = 10
        unloadCost = 15
        sailCost = 35
        estimate = (loadCost + unloadCost) * len(state.ports[0])
        estimate += unloadCost * state.boat.get_container_stowage()
        if state.boat.port == 0:
            estimate += 2 * sailCost
        return estimate

    def getEstimation(self, state):
        loadCost = 10
        unloadCost = 15
        sailCost = 35
