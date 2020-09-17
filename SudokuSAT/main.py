import sat_solver
import time


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


def load_txt(file): # transform a sudoku into cnf
    f = open(file, 'r')
    data = f.read()
    f.close()
    cnf = []
    for i in range(1, 10):
        for j in range(1, 10):
            if data[0] != '.':
                cnf.append([i*100 + j*10 + int(data[0])])
            data = data[1:]
    return cnf


def print_sudoku_grid(sol):
    for i in range(0, 81):
        print(sol[i] % 10, end=' ')
        if (i + 1) % 9 == 0:
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


def load_many_sudokus(file, rules):
    f = open(file, 'r')
    data = f.read()
    f.close()
    lines = data.split("\n")
    for line in lines:
        cnf = []
        for i in range(1, 10):
            for j in range(1, 10):
                if line[0] != '.':
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
        print('Time: ', end - start)
        print_sudoku_grid(sol)


rules = load_dimacs('sudoku-rules.txt')
load_many_sudokus('sat_tests/sudoku_txt/1000 sudokus.txt', rules)


# sudoku = load_txt('sat_tests/sudoku_txt/sudoku5.txt')
# # sudoku = load_dimacs('sat_tests/sudoku_dimacs/sudoku2')
# rules = load_dimacs('sudoku-rules.txt')
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
