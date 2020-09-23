import sat_solver
import time
import pandas as pd
import numpy as np
import math


def load_dimacs(file):
    f = open(file, 'r')  # open file in reading mode
    data = f.read()  # read file in data variable; string type
    f.close()
    lines = data.split("\n")  # split the data into a list of lines
    cnf = []
    for line in lines:
        if len(line) == 0 or line[0] in ['c', 'p', '%', '0']:
            continue  # ignore the lines without clauses
        clause = [int(x) for x in line.split()[:-1]]  # transform the string clause format into a int one, remove the last 0;
        cnf.append(clause)  # add the clause to the list
    return cnf


def load_rules(rules_nr):
    if rules_nr == 1:
        rules = load_dimacs('sat_tests/sudoku_rules/sudoku-rules-4x4.txt')
    elif rules_nr == 2:
        rules = load_dimacs('sat_tests/sudoku_rules/sudoku-rules-9x9.txt')
    else:
        rules = load_dimacs('sat_tests/sudoku_rules/sudoku-rules-16x16.txt')
    return rules


def sudoku_grid(sol, dim):
    sudoku = ''
    for i in range(0, dim * dim):
        sudoku += str(sol[i] % 10)
        if (i + 1) % dim == 0:
            sudoku += '\n'
    grid = np.array([[int(i) for i in line] for line in sudoku.split()])
    return grid


def write_output(sol):
    output = open('file.out', 'w')
    for element in sol:
        output.write(str(element) + ' 0 \n')
    output.close()


def check_sudoku(grid, dim):
    """ Return True if grid is a valid Sudoku square, otherwise False. """
    sqrt_dim = int(math.sqrt(dim))
    for i in range(dim):
        # j, k index top left hand corner of each 3x3 tile
        j, k = (i // sqrt_dim) * sqrt_dim, (i % sqrt_dim) * sqrt_dim
        if len(set(grid[i, :])) != dim or len(set(grid[:, i])) != dim \
                or len(set(grid[j:j+sqrt_dim, k:k+sqrt_dim].ravel())) != dim:
            return False
    return True


def load_many_sudokus(file, rules, dim, sudoku_amount):
    average_time = 0
    average_nr_of_splits = 0
    average_nr_of_backtracks = 0
    h = input('Choose heuristic (0 - none, 1 - random, 2 - DLIS, 3 - DLCS, 4 - min heur or 5 - JW): ')
    h = int(h)
    f = open(file, 'r')
    data = f.read()
    f.close()
    lines = data.split("\n")
    counter = 1
    dataset = pd.DataFrame(columns=['ID', 'Heuristic', 'Time', 'Nr of Splits', 'Nr of Backtracks'])
    for line in lines:
        if counter < sudoku_amount+1:
            cnf = []
            for i in range(1, dim + 1):
                for j in range(1, dim + 1):
                    if len(line) != 0 and line[0] != '.':
                        cnf.append([i * 100 + j * 10 + int(line[0])])
                    line = line[1:]
            cnf += rules
            sol = []
            start = time.time()
            sat_solver.dp(cnf, sol, h)
            end = time.time()
            sol.sort()
            print('Sudoku solution: ', sol)
            total_time = end - start
            print('Time: ', total_time)
            grid = sudoku_grid(sol, dim)
            print(grid)
            print('Solution check: ', check_sudoku(grid, dim))
            dataset = dataset.append({'ID': counter, 'Heuristic': sat_solver.heur, 'Time': total_time, 'Nr of Splits': sat_solver.nrofSplits_tosave, 'Nr of Backtracks': sat_solver.nrofBacktracks_tosave}, ignore_index=True)
            average_time += total_time
            average_nr_of_splits += sat_solver.nrofSplits_tosave
            average_nr_of_backtracks += sat_solver.nrofBacktracks_tosave
            counter += 1

    print(dataset)
    filename = f'sat_solver_{h}.xls'
    dataset.to_excel(filename, index=False)
    print('Average time: ', average_time / sudoku_amount)
    print("Average nr of splits: ", average_nr_of_splits / sudoku_amount)
    print('Average nr of backtracks: ', average_nr_of_backtracks / sudoku_amount)
    dataset_avg = dataset.append({'Average time': average_time / sudoku_amount, 'Average nr of splits': average_nr_of_splits / sudoku_amount, 'Average nr of backtracks': average_nr_of_backtracks / sudoku_amount}, ignore_index=True)
    dataset_avg.to_excel(filename, index=False)


dimension = input('Choose sudoku dimension (4 or 9): ')
dimension = int(dimension)
if dimension == 4:
    rules = load_rules(1)
    load_many_sudokus('sat_tests/sudoku_txt/4x4hard.txt', rules, dimension, 500)
elif dimension == 9:
    rules = load_rules(2)
    load_many_sudokus('sat_tests/sudoku_txt/damnhard.sdk.txt', rules, dimension, 50)
elif dimension == 16:
    rules = load_rules(3)
    load_many_sudokus('sat_tests/sudoku_txt/16x16.txt', rules, dimension, 5)
