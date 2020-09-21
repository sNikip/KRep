from sat_solver import *
import sat_solver
import time
import pandas as pd
import numpy as np


def load_dimacs(file):
    f = open(file, 'r') # open file in reading mode
    data = f.read() # read file in data variable; string type
    f.close()
    lines = data.split("\n") # split the data into a list of lines
    cnf = []
    for line in lines:
        if len(line) == 0 or line[0] in ['c', 'p', '%', '0']:
            continue # ignore the lines without clauses
        clause = [int(x) for x in line.split()[:-1]] # transform the string clause format into a int one, remove the last 0;
        cnf.append(clause) # add the clause to the list
    return cnf


# def load_txt(file): # transform a sudoku into cnf
#     f = open(file, 'r')
#     data = f.read()
#     f.close()
#     cnf = []
#     for i in range(1, 10):
#         for j in range(1, 10):
#             if data[0] != '.':
#                 cnf.append([i*100 + j*10 + int(data[0])])
#             data = data[1:]
#     return cnf


def load_rules(rulesNr):
    if rulesNr == 1:
        rules = load_dimacs('sat_tests/sudoku_rules/sudoku-rules-4x4.txt')
    elif rulesNr == 2:
        rules = load_dimacs('sat_tests/sudoku_rules/sudoku-rules-9x9.txt')
    else:
        rules = load_dimacs('sat_tests/sudoku_rules/sudoku-rules-16x16.txt')
    return rules


def print_sudoku_grid(sol, x):
    for i in range(0, x*x):
        print(sol[i] % 10, end=' ')
        if (i + 1) % x == 0:
            print('\n', end='')


def write_output(sol):
    output = open('file.out', 'w')
    for element in sol:
        output.write(str(element) + ' 0 \n')
    output.close()


def check_if_missing(sol):
    lag = 0
    for i in range(0, len(sol)):
        cell = i + 11 + (i // 9)
        if sol[i - lag] // 10 != cell:
            print('Missing: ', end='')
            print(cell)
            lag = lag + 1



def load_many_sudokus(file, rules, x, sudokuAmount):
    f = open(file, 'r')
    data = f.read()
    f.close()
    lines = data.split("\n")
    counter = 1
    dataset = pd.DataFrame(columns=['ID', 'Heuristic', 'Time', 'Nr of Splits','Nr of Backtracks', 'Amout of Putnam Calls'])
    for line in lines:
        if (counter < sudokuAmount +1):
            cnf = []
            for i in range(1, x+1):
                for j in range(1, x+1):
                    if len(line) != 0 and line[0] != '.':
                        cnf.append([i * 100 + j * 10 + int(line[0])])
                    line = line[1:]
            cnf += rules
            start = time.time()
            sol = []
            print(sat_solver.dp(cnf, sol))
            sol.sort()
            print('Sudoku solution: ', sol)
            print('Solution length: ', len(sol))
            end = time.time()
            Total_time = end - start
            print('Time: ', Total_time)
            print_sudoku_grid(sol, x)
            dataset = dataset.append({'ID': counter, 'Heuristic': sat_solver.heur, 'Time': Total_time, 'Nr of Splits': sat_solver.nrofSplits_tosave, 'Nr of Backtracks': sat_solver.nrofBacktracks_tosave, 'Amout of Putnam Calls': sat_solver.putnamCalls}, ignore_index=True)
            counter +=1
    print(dataset)
    filename = f'sat_solver_DLIS.xls'
    dataset.to_excel(filename, index = False)



x = input('Choose sudoku dimension (4 or 9): ')
x = int(x)
if x == 4:
    rules = load_rules(1)
    load_many_sudokus('sat_tests/sudoku_txt/4x4.txt', rules, x, 5)
elif x == 9:
    rules = load_rules(2)
    load_many_sudokus('sat_tests/sudoku_txt/1000 sudokus.txt', rules, x, 2)
elif x == 16:
    rules = load_rules(3)
    load_many_sudokus('sat_tests/sudoku_txt/16x16.txt', rules, x, 5)





# sudoku = load_txt('sat_tests/sudoku_txt/sudoku5.txt')
# # sudoku = load_dimacs('sat_tests/sudoku_dimacs/sudoku2')
# rules = load_dimacs('sudoku-rules-9x9.txt')
# cnf = sudoku + rules


# start = time.time()
# sol = []
# print(sat_solver.dp(cnf, sol))
# sol.sort()
# print('Sudoku solution: ', sol)
# print('Solution length: ', len(sol)) # length > 81 means there are multiple solutions
# end = time.time()
# print('Time: ', end - start)
#
#
# check_if_missing(sol)
#
# print_sudoku_grid(sol)
# write_output(sol)
