from state import State
from action import Action, Load, Sail, Unload
from search.search import SearchProblem


class Stowage(SearchProblem):
    def __init__(self, file_containers, file_layout):
        state = State.get_init_goal(file_containers, file_layout)
        initial_state = state.get_Init()
        goal_state = state.get_Final()
        super().__init__(initial_state, goal_state)

    def getLegalActions(self, state):
        return self.get_valid_actions(state)

    def get_valid_actions(self, state):
        #TODO: get possible actions by checking preconditions

        """
        :param state: current state (port, boat)
        :return: list of objects Actions: Load, Sail, Unload, with the
        necessary paramenters which can be applied from state
        """

        #action = Load(cost, port, c, cell) /
        #action = Sail(cost, port_init, port_final)
        #action = Unload(cost, port, c, cell)

        pass

    def getSuccessors(self, state):
        succesors = []

        for action in self.getLegalActions(state):
            newstate = action.applyAction(state)
            action = action.__str__()
            stepCost = action.cost
            succesors.append((newstate, action, stepCost))

        return succesors


