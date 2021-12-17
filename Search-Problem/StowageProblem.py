from state import State
from action import Load, Sail, Unload
from search.search import SearchProblem


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

        #sail
        all_act = [Sail(0, 1), Sail(1, 2)]
        #load/unload from port 0/1/2
        for p in range(2):
            #obtain tuples of containers
            for cont in self.containers:
                #obtain each cell of boat stowage
                for cell in self.layout:
                    all_act.append(Load(p, cont, cell))
                    all_act.append(Unload(p, cont, cell))
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
            action = action.__str__()
            stepCost = action.cost
            succesors.append((newstate, action, stepCost))

        return succesors

    def getCostOfActions(self, actions):
        return [action.costAction() for action in actions]

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
        estimate = (loadCost + unloadCost)*len(state.ports[0])
        estimate += unloadCost * state.boat.get_container_stowage()
        if state.boat.port == 0:
            estimate += 2 * sailCost
        return estimate

    def getEstimation(self, state):
        loadCost = 10
        unloadCost = 15
        sailCost = 35






