import enum

# actions are ordered according to clockwise
class Action(enum.Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    # because of actions are clockwise ordered in my code, and we have to choose according to action preference order 
    # that speficied in homework documentation, then I wrote this method for selecting action according to this preference order
    @staticmethod
    def selectAction(q_values):
        # q values normally ordered as up, right, down, left
        # ordering q_values according to action preference order
        preference_order = [q_values[0],q_values[2],q_values[1],q_values[3]] # now ordered list became up, down, right, left
        max_value = max(preference_order)
        action_preference = [Action.UP, Action.DOWN, Action.RIGHT, Action.LEFT]
        return action_preference[preference_order.index(max_value)]

class CellType(enum.Enum):
    INITIAL = 1 # this is also non-terminal but special one
    NON_TERMINAL = 2
    GOAL = 3
    PENALTY = 4
    WALL = 5
