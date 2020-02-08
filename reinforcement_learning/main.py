from grid import Grid
from mdp import MarkovDecision
from q_learning import QLearning
import numpy as np

def main():

    # initialization of the grid
    grid = Grid() 

    # creating markov decision and q learning classes for using algorithms
    mdp = MarkovDecision() 
    ql = QLearning()

    print("\n")
    print("Value iteration results: \n")
    # parameter order: p, reward, discount
    utilities, policies = mdp.iterateValues(grid, 1,0,1)
    grid.printPolicies()

    grid.resetGrid()

    print("\n")
    print("Policy iteration results: \n")
    # parameter order: p, reward, discount
    mdp.iteratePolicies(grid,1,0,1)
    grid.printPolicies()

    grid.resetGrid()
    
    print("\n")
    print("Q Learning results: \n")
    #parameter order: grid, p, reward, learning_rate, discount, epsilon, iteration, value_iteration results 
    ql.learnQ(grid, 1, 0, 0.1, 1, 0, 1000, utilities, policies)
    grid.printQValues()
    grid.printQLearningResults()


main()

