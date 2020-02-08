from gridworld_enums import Action

# this class for performing markov decision process algorithms like value iteration and policy iteration
class MarkovDecision:

    # this method stands for calculating q(s,a) value
    def computeQValue(self, grid, state, action, reward, discount):
        possible_states = grid.getPossibleStates(state, action)
        value = 0.0
        for i in range(len(possible_states)):
            value += possible_states[i].getValue() * grid.transitions[i]
        
        return reward + discount * value

    # this method detects the convergence in the value iteration or policy evaluation
    def isConverged(self, current_value, previous_value, discount, error):
        difference_value = abs(current_value - previous_value)
        if discount < 1:
            if(difference_value < error * (1-discount) / 2 * discount):
                return True
        elif discount == 1:
            if(difference_value < error / 2):
                return True
        return False
    
    def iterateValues(self, grid, p, reward, discount):
        grid.initializeTransitions(p)
        non_terminal_states = grid.getNonTerminalStates()
        iteration_results = [[i.getValue() for i in non_terminal_states]] # for storing each iteration result
        converged_state_count = 0 # will increase if one of the value is converged

        while(converged_state_count < 11):
            new_values = []
            new_actions = []
            converged_state_count = 0
            for state in non_terminal_states:
                q_values = []
                for action in Action:
                    value = self.computeQValue(grid, state, action, reward, discount)
                    q_values.append(value)
                # selecting max q_value and action phase
                max_q = max(q_values)
                max_action = Action.selectAction(q_values) # policy extraction
                new_values.append(max_q)
                new_actions.append(max_action)

                if(self.isConverged(max_q, state.getValue(), discount, 1e-5) == True):
                    converged_state_count += 1    
            
            iteration_results.append(new_values) # appending iteration results of iteration
            # updating values and policies
            grid.updateValues(non_terminal_states, new_values)
            grid.updatePolicies(non_terminal_states, new_actions)
        grid.printResults(iteration_results)
        return [i.getValue() for i in non_terminal_states], [i.getPolicy() for i in non_terminal_states]

    def iteratePolicies(self, grid, p, reward, discount):
        grid.initializeTransitions(p)
        non_terminal_states = grid.getNonTerminalStates()
        converged_policy = 0 # will increase if one of the policies is converged
        iteration_results = [[i.getValue() for i in non_terminal_states]] # for storing each iteration result
        
        while(converged_policy < 11):
            new_actions = []
            converged_policy = 0
            # policy evaluation step
            converged_value = 0 
            # iterate values by using assigned policies until converge
            while(converged_value < 11):
                policy_values = []
                for state in non_terminal_states:
                    value = self.computeQValue(grid,state, state.getPolicy(), reward, discount) 
                    policy_values.append(value)
                    if(self.isConverged(value, state.getValue(), discount, 1e-5) == True):
                        converged_value += 1         
                grid.updateValues(non_terminal_states, policy_values) 
            iteration_results.append(policy_values)
            # policy improvement step
            # if there is better policy then update the policy
            for state in non_terminal_states:
                q_values = []
                for action in Action:
                    arg_value = self.computeQValue(grid,state, action, reward, discount)
                    q_values.append(arg_value)
                max_action = Action.selectAction(q_values)
                new_actions.append(max_action)

                if(state.getPolicy() == max_action):
                    converged_policy += 1
                else:
                    state.setPolicy(max_action) # updating policy of state
            grid.updatePolicies(non_terminal_states, new_actions)
        grid.printResults(iteration_results)
