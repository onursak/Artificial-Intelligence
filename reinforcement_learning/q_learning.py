import numpy as np
from grid import Grid
from gridworld_enums import CellType
from gridworld_enums import Action

np.random.seed(62)

# this class for performing q learning algorithm
class QLearning:
    # returns the possible future state and corresponding direction, I named it randomly because of transition
    def moveRandomly(self, possible_states, possible_actions):
        transition_value = float(np.random.rand())
        if transition_value >= 0 and transition_value <= 0.8:
            return possible_states[0], possible_actions[0]
        elif transition_value > 0.8 and transition_value < 0.9:
            return possible_states[2], possible_actions[2]
        else:
            return possible_states[1], possible_actions[1]
    
    # moves the agent for exploring
    def moveExplore(self, grid, current_state):
        actions = [Action.UP, Action.DOWN, Action.RIGHT, Action.LEFT]
        random_value = int(np.random.randint(0,4))
        action = actions[random_value]
        possible_actions = grid.getPossibleActions(action)
        possible_states = grid.getPossibleStates(current_state, action)
        return self.moveRandomly(possible_states, possible_actions)

    # moves the agent for exploitation
    def moveExploit(self, grid, current_state):
        action = current_state.getMaxAction()
        possible_actions = grid.getPossibleActions(action)
        possible_states = grid.getPossibleStates(current_state, action)
        return self.moveRandomly(possible_states, possible_actions)

    # this function stands for applying q learning algorithm
    def learnQ(self, grid, p, reward, learning_rate, discount, epsilon, iteration, value_iteration_values, value_iteration_policies):
        grid.initializeTransitions(p)
        iteration_count = 0
        agent_state = grid.getInitialState()
        hundred_iteration_results = []
        while(iteration_count < iteration):
            future_state = 0
            direction = 0
        
            # this loop stands for episode(reaching goal or penalty)
            while(True):
                # if random value smaller than epsilon then explore the environment(e-greedy), otherwise exploit
                if float(np.random.rand()) < epsilon:
                    future_state, direction = self.moveExplore(grid, agent_state)
                else:
                    future_state, direction = self.moveExploit(grid, agent_state)
                new_value = 0
                if future_state.getType() == CellType.GOAL or future_state.getType() == CellType.PENALTY:
                    new_value = (agent_state.getQValue(direction) 
                            + learning_rate * (future_state.getValue() - agent_state.getQValue(direction)))
                    agent_state.updateQValue(direction, new_value)  # q value update rule
                    agent_state = grid.getInitialState() # we reached the goal or penalty(episode ended), then agent starts from initial state again
                    break
                else:
                    new_value = (agent_state.getQValue(direction) 
                            + learning_rate * (reward + discount * future_state.getMaxQ() - agent_state.getQValue(direction))) # q value update rule
                    agent_state.updateQValue(direction, new_value) 
                    agent_state = future_state # move the agent to the future state then continue to episode
            last_iteration = False
            if(iteration_count+2 > iteration - 100):
                last_iteration = True
            if((iteration_count+1) % 100 == 0):
                current_results = [i.getMaxQ() for i in grid.getNonTerminalStates()]
                current_policies = [i.getMaxAction() for i in grid.getNonTerminalStates()]
                hundred_iteration_results.append(current_results)
                grid.plotErrors(value_iteration_values, value_iteration_policies, current_results, current_policies, last_iteration)
            iteration_count += 1
        return hundred_iteration_results
    