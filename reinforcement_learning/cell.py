from gridworld_enums import Action
from gridworld_enums import CellType

# Class that contains cell/state information and methods
class Cell:
    def __init__(self, cell_number, cell_type, value = 0.0, policy = Action.UP):
        self.cell_number = cell_number
        self.value = value
        self.policy = policy
        self.cell_type = cell_type
        self.q_values = [0.0,0.0,0.0,0.0]
    
    def getCellNumber(self):
        return self.cell_number
    
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
    
    def getPolicy(self):
        return self.policy
    
    def setPolicy(self, policy):
        self.policy = policy
    
    def getType(self):
        return self.cell_type
    
    def getRow(self):
        return self.cell_number // 4
    
    def getColumn(self):
        return self.cell_number % 4
    
    def getCoordinates(self):
        return self.getRow(), self.getColumn()
    
    def setQValues(self, q_values):
        self.q_values = q_values
    
    # returning action that has highest q value, according to action preference order
    def getMaxAction(self):
        return Action.selectAction(self.q_values)

    # returns the q value corresponding to specific direction
    def getQValue(self, direction):
        if direction == Action.UP:
            return self.q_values[0]
        elif direction == Action.RIGHT:
            return self.q_values[1]
        elif direction == Action.DOWN:
            return self.q_values[2]
        elif direction == Action.LEFT:
            return self.q_values[3]

    # returns the max q value of the state
    def getMaxQ(self):
        return max(self.q_values)

    # updates q value of specific direction with new value
    def updateQValue(self, direction, value):
        if direction == Action.UP:
            self.q_values[0] = value
        elif direction == Action.RIGHT:
            self.q_values[1] = value
        elif direction == Action.DOWN:
            self.q_values[2] = value
        elif direction == Action.LEFT:
            self.q_values[3] = value