from crooksAlgorithm import loop_basic_rule, loop_algorithm, check_box_eliminate_others
from sudokuSolver import solve, find_empty
import copy
from sudokuGenerator import createBoard
import time
# Input excel file path and sheet name

question = createBoard()
question2 = question.copy()

    

def solveByCrooks(question):
       
        # Copy existing information from question
        solution = copy.deepcopy(question)
        possible_value = {}
        
        # Cell notation [i, j] i , j: from 1 to 9
        # First is to include all possible numbers for each cell
        for i in range(1, 10):
            for j in range(1, 10):
                possible_value[i, j] = list(range(1, 10))
        
        # If the cell is already filled, remove all possible numbers for this cell
        for i in range(1, 10):
            for j in range(1, 10):
                if solution[i - 1][j - 1] != 0:
                    possible_value[i, j] = []
        
        # Run basic rules and Crook's algorithm
        while True:
            solution_old = copy.deepcopy(solution)
            loop_basic_rule(possible_value, solution)
            loop_algorithm(possible_value, solution)
            check_box_eliminate_others(possible_value)
            if solution == solution_old:
                break
        
        # Check if the final result is solution
        if find_empty(solution)==None:
            return solution
        else:
            solve(solution)
        
        
        return solution
