import pandas as pd
import numpy as np
from gridworld_enums import CellType
from cell import Cell
from gridworld_enums import Action
import matplotlib.pyplot as plt


# class that contains all of the information about the grid like states, transitions
class Grid:
    def __init__(self):
        self.states = self.initializeGrid()
        self.transitions = []
    
    # initiliazition method for creating states of the grid
    def initializeGrid(self):
        grid = [[0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]]
        for i in range(0,16):
            row, column = self.convertToCoordinate(i)
            grid[row][column] = Cell(i, CellType.NON_TERMINAL)
        initial = Cell(8, CellType.INITIAL)
        goal_1 = Cell(3, CellType.GOAL, 1)
        goal_2 = Cell(13, CellType.GOAL, 1)
        goal_3 = Cell(15, CellType.GOAL, 10)
        penalty = Cell(14, CellType.PENALTY, -10)
        wall = Cell(5, CellType.WALL)
        states = [initial, goal_1, goal_2, goal_3, penalty, wall]
        for i in states:
            row, column = i.getCoordinates()
            grid[row][column] = i
        return grid

    def initializeTransitions(self, p):
        self.transitions = [p, (1-p) / 2, (1-p) / 2]

    def getActions(self):
        return [i for i in Action]
    
    def getInitialState(self):
        for i in self.states:
            for j in i:
                if j.getType() == CellType.INITIAL:
                    return j

    # this method for converting cell number to the coordinate information on the grid
    def convertToCoordinate(self, cell_number):
        row = cell_number // 4
        column = cell_number % 4
        return row,column
    
    # this method for converting grid world coordinate to the cell number
    def convertToNumber(self, coordinates):
        row = coordinates[0]
        column = coordinates[1]
        return row * 4 + column
    
    # this method for resetting the grid values after applying any algorithms
    def resetGrid(self):
        self.states = self.initializeGrid()
        
    # returns the non terminal states of the grid    
    def getNonTerminalStates(self):
        non_terminals = []
        for i in self.states:
            for j in i:
                if j.getType() == CellType.INITIAL or j.getType() == CellType.NON_TERMINAL:
                    non_terminals.append(j)
        return non_terminals
    
    # for printing grid values in 4x4 matrix
    def printGridValues(self):
        values = []
        for i in self.states:
            temp = []
            for j in i:
                if j.getType() == CellType.WALL:
                    temp.append("WALL")
                else:
                    temp.append(j.getValue())
            values.append(temp)
        df = pd.DataFrame(values)
        print(df)

    # for printing grid policies in 4x4 matrix
    def printPolicies(self):
        policies = []
        for i in self.states:
            temp = []
            for j in i:
                if j.getType() == CellType.WALL:
                    temp.append("WALL")
                elif j.getType() == CellType.GOAL or j.getType() == CellType.PENALTY:
                    temp.append(j.getValue())
                else:
                    temp.append(j.getPolicy().name)
            policies.append(temp)
        df = pd.DataFrame(policies)
        print(df)
        
    def printResults(self, results):
        df = pd.DataFrame(results, columns=['s0', 's1', 's2','s3', 's4', 
                                   's5','s6', 's7', 's8',
                                   's9', 's10'])
        print(df)
    
    def printQLearningResults(self):
        for i in self.getNonTerminalStates():
            max_action = i.getMaxAction()
            i.setPolicy(max_action)
        self.printPolicies()

    def printQValues(self):
        q_values = []
        for i in self.getNonTerminalStates():
            q_values.append(i.q_values)
        df = pd.DataFrame(q_values, columns=['up_q', 'right_q', 'down_q','left_q'])
        print(df)

    def getStateWithCoordinate(self, row, column):
        if row > 3 or row < 0:
            return None
        
        elif column > 3 or column < 0:
            return None
        
        return self.states[row][column]
    
    # simply returns the next state, if there is a wall returns False, otherwise next state
    def getNextState(self, state, action):
        
        control_state = 0
        if action == Action.UP:
            control_state = self.getStateWithCoordinate(state.getRow()-1, state.getColumn())
        elif action == Action.RIGHT:
            control_state = self.getStateWithCoordinate(state.getRow(), state.getColumn()+1)
        elif action == Action.LEFT:
            control_state = self.getStateWithCoordinate(state.getRow(), state.getColumn()-1)
        elif action == Action.DOWN:
            control_state = self.getStateWithCoordinate(state.getRow()+1, state.getColumn())
        
        if control_state == None or control_state.getType() == CellType.WALL:
            return False
        
        return control_state
    
    # returns possible actions according to transition rule, for example if we want to go right then this method returns [right, down, up]
    def getPossibleActions(self, action):
        actions = self.getActions()
        action_index = actions.index(action)
        possible_right = actions[(action_index+1)%4]
        possible_left = actions[(action_index-1)%4]    
        return [action, possible_right, possible_left]
    
    # returns possible states according to possible actions
    def getPossibleStates(self, state, action):
        possible_actions = self.getPossibleActions(action)
        possible_states = []
        for i in possible_actions:
            control = self.getNextState(state, i)
            # if there is a wall, then append state itself
            if control == False:
                possible_states.append(state)
            else:
                possible_states.append(control)
        return possible_states
    
    # updates grid values with the new ones
    def updateValues(self, non_terminal_states, newValues):
        for i in range(len(non_terminal_states)):
            row, column = non_terminal_states[i].getCoordinates()
            state = self.states[row][column]
            state.setValue(newValues[i])
            
    # updates grid policies with the new ones
    def updatePolicies(self, non_terminal_states, newPolicies):
        for i in range(len(non_terminal_states)):
            row, column = non_terminal_states[i].getCoordinates()
            state = self.states[row][column]
            state.setPolicy(newPolicies[i])
           
    def plotErrors(self, results, value_policies, q_learning_results, q_learning_policies, last_iteration):
        error_results = []
        error_results_policies = []
        state_numbers = [i for i in range(0,11)]

        for i in range(len(q_learning_results)):
            error_results.append(abs(q_learning_results[i] - results[i]))
        
        for i in range(len(q_learning_policies)):
            error_results_policies.append(abs(q_learning_policies[i].value - value_policies[i].value))

        plt.plot(state_numbers, error_results, 'b');
        plt.plot(state_numbers, error_results_policies,'g')
        plt.legend(['utility error', 'policy error'], loc='upper left')

        if last_iteration == True:
            plt.show()
        else:
            plt.pause(0.001)
            plt.clf()

    